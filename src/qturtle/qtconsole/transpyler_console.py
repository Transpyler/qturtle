
import uuid
from collections import deque
from logging import getLogger

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from jupyter_client.localinterfaces import is_local_ip
from lazyutils import lazy
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

from transpyler import Transpyler
from transpyler.jupyter.app import TranspylerKernelManager
from transpyler.jupyter.setup import setup_assets
from qturtle import colors
from qturtle.mixins import TranspylerConsoleMixin

###Qtconsole
from .itranspyler_qt_consoleapp import ITranspylerQtConsoleApp
from .styles import dark_style_sheet, dark_syntax_style, dark_style_template
from .itranspyler_widget_qt_consoleapp import ITranspylerWidgetQtConsoleApp 

###


log = getLogger('gui.ipytuga')
_ = lambda x: x


class TranspylerConsole(TranspylerConsoleMixin, QtWidgets.QWidget):
    """
    A Jupyter transpyler console that can be embedded in a ReplWidget.
    """

    printToConsoleSignal = QtCore.pyqtSignal(str, bool)
    turtleMessageSignal = QtCore.pyqtSignal(object)

    def __init__(self, transpyler, parent=None, **kwargs):
        super().__init__(transpyler=transpyler, parent=parent, **kwargs)
        self._app = ITranspylerWidgetQtConsoleApp(transpyler=transpyler)
        self._widget = self._app.widget
        self._turtle_mailbox_comm_id = None
        self._inbox_messages = deque()
        self._inbox_handlers = {}
        self._msg_handlers = {}
        self._app.kernel_client.iopub_channel.message_received.connect(
            self.messageEvent)

    def __del__(self):
        # Kills kernel when console is destroyed
        self._app.kernel_manager.shutdown_kernel(now=True)

    def initNamespace(self):
        if self._turtle_mailbox_comm_id is None:
            self.initTurtleComm()

        self.runCodeSilent(
            'from qturtle.kernel import init_namespace\n'
            'init_namespace(get_ipython().kernel.transpyler, globals())\n'
            'del init_namespace\n'
            'forward(0)  # create default turtle\n'
        )

    def initTurtleComm(self):
        """
        Create Comm link between Gui application and the kernel.
        """

        client = self._app.kernel_client

        # Register comm handler in the kernel
        self.runCodeSilent(
            'from qturtle.kernel import comm as _comm\n'
            '_comm(get_ipython())\n'
        )

        # Now sends a comm_open message through the shell channel. This
        # opens the handler and starts communication
        type = 'comm_open'
        self._turtle_mailbox_comm_id = str(uuid.uuid1())
        payload = {
            'comm_id': self._turtle_mailbox_comm_id, 'target_name': 'turtles'
        }
        msg = client.session.msg(type, payload)

        # The default handler in the kernel should send an acknowledge message.
        # We should listen to it in the iopub channel.
        def confirm_comm_open(msg):
            if msg != ['comm_open']:
                raise ValueError('got invalid response to comm_open: %s' % msg)

        msg_id = msg['header']['msg_id']
        self.registerMailboxHandler(msg_id, confirm_comm_open)
        client.shell_channel.send(msg)

    def messageEvent(self, msg):
        """
        Handles incomming messages in the comm channel.
        """

        msg_type = msg['msg_type']

        if msg_type == 'comm_msg':
            data = msg['content']['data']
            id = msg['parent_header']['msg_id']
            comm_id = msg['content']['comm_id']

            # Treat messages with registered handlers immediately
            if id in self._inbox_handlers:
                handler = self._inbox_handlers.pop(id)
                handler(data)
                return
            elif comm_id == self._turtle_mailbox_comm_id:
                data = msg['content']['data']
                self.turtleMessageSignal.emit(data)
            else:
                raise ValueError('invalid comm_id: %s' % data)

    def registerMailboxHandler(self, id, handler):
        """
        Register a callback for a message with the given id.
        """
        self._inbox_handlers[id] = handler

    def handleMessageReply(self, data):
        """
        Receives a message reply from the turtle server (usually the scene
        object). This reply should be sent back to the kernel using the open
        comm.
        """

        client = self._app.kernel_client
        payload = {
            'comm_id': self._turtle_mailbox_comm_id, 'data': data
        }
        msg = client.session.msg('comm_msg', payload)
        client.shell_channel.send(msg)

    def runCodeSilent(self, code):
        self._app.execute(code, silent=True, stop_on_error=False)

    def runCode(self, code, hidden=False, interactive=True, short=True):
        if not code.strip():
            return

        if '\n' in code and short:
            self._widget.execute('', hidden, interactive)
            self.runCodeSilent("print('...')")
            self.runCodeSilent(code)
        else:
            self._widget.execute(code, hidden, interactive)

    def setTheme(self, theme):
        self._app.set_theme(theme)

    def widget(self):
        return self._widget

    def _font_diff(self, diff):
        font = self._widget.font
        size = font.pointSize()
        font.setPointSize(size + diff)
        self._widget.font = font

    def zoomIn(self):
        self._font_diff(1)

    def zoomOut(self):
        self._font_diff(-1)

    def zoomTo(self, factor):
        font = self._widget.font
        font.setPointSize(10 + factor)
        self._widget.font = font

