import builtins
import functools
import io
import sys
import time
import traceback

from PyQt5 import QtCore


class TranspylerRunner(QtCore.QObject):
    # Signals
    askInputSignal = QtCore.pyqtSignal(str)
    askAlertSignal = QtCore.pyqtSignal(str)
    askFileSignal = QtCore.pyqtSignal(bool)
    pauseExecutionSignal = QtCore.pyqtSignal()
    resumeExecutionSignal = QtCore.pyqtSignal()
    receiveInputSignal = QtCore.pyqtSignal(str)

    def __init__(self, transpyler, namespace=None):
        super().__init__()
        self._transpyler = transpyler
        self._waiting = False
        self._userinput = None
        self.resumeExecutionSignal.connect(self._resumeExecution)
        self.receiveInputSignal.connect(self._receiveInput)
        self._namespace = dict(namespace or {})
        self._update_special_functions()
        self._exec = transpyler.exec

    def _update_special_functions(self):
        @functools.wraps(input)
        def input_function(msg=None):
            self._waiting = True
            self._userinput = None
            self.askInputSignal.emit(str(msg or ''))
            while self._waiting:
                time.sleep(0.05)
            return self._userinput

        def alert(*args, sep=' ', end='\n'):
            """Opens an alert dialog displaying the input message."""

            data = sep.join(map(str, args)) + end
            self._waiting = True
            self.askAlertSignal.emit(data)
            while self._waiting:
                time.sleep(0.05)

        def pause():
            """Opens a dialog that pauses execution until the user cancels
            it."""
            self._waiting = True
            self.pauseExecutionSignal.emit()
            while self._waiting:
                time.sleep(0.05)

        def filechooser(do_open):
            self._waiting = True
            self._userinput = None
            self.askFileSignal.emit(do_open)
            while self._waiting:
                time.sleep(0.05)
            return self._userinput

        builtins.input = input_function
        self._namespace['input'] = input_function
        self._namespace['alert'] = alert
        self._namespace['pause'] = pause
        self._namespace['filechooser'] = filechooser

    def _resumeExecution(self):
        self._waiting = False

    def _receiveInput(self, value):
        self._userinput = value
        self._resumeExecution()

    def transpyler(self):
        return self._transpyler

    def setNamespace(self, ns):
        self._namespace.update(ns)

    def checkComplete(self, src):
        """
        Return True if source code can represent a complete command.
        """
        header, *_ = src.splitlines()
        return header.strip().endswith(':')

    def checkValidSyntax(self, src):
        """
        Return True if source code has a valid syntax.
        """
        try:
            compile(self.transform(src), '<input>', 'eval')
            return True
        except SyntaxError:
            return False

    def runSingle(self, src):
        """
        Runs command in 'single' mode: returns a string with the representation
        of the command output.
        """
        return self._run_worker(src, 'single', self._namespace)

    def runExec(self, src):
        """
        Runs command in "exec" mode: returns a string with all prints during
        the command's execution.
        """
        return self._run_worker(src, 'exec', self._namespace)

    def kill(self):
        """
        Kills runner processs
        """
        raise NotImplementedError

    def poll(self):
        """Poll runner and return a boolean telling if runner is running"""

        return False

    def transform(self, src):
        return src

    def updateNamespace(self, D):
        self._namespace.update(D)

    def cancel(self):
        """
        Cancel execution of a runner process
        """
        raise NotImplementedError

    def _run_worker(self, cmd, mode, ns):
        stdout, stderr = sys.stdout, sys.stderr
        out = sys.stdout = io.StringIO()
        err = sys.sterr = io.StringIO()
        try:
            code = compile(self.transform(cmd), '<input>', mode)
            self._exec(code, ns)
        except:
            traceback.print_exc(file=out)
        finally:
            sys.stdout, sys.stderr = stdout, stderr
            data = out.getvalue() + err.getvalue()
            return data

    def _set_subprocess_globals(self, namespace):
        D = globals()
        D.update(namespace)
