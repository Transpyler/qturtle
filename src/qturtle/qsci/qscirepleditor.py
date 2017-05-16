from .qsciconsole import TranspylerConsole
from .qscieditor import TranspylerEditor
from ..repleditor import ReplEditor


class QsciReplEditor(ReplEditor):
    def _createConsoleApp(self):
        return TranspylerConsole(self.transpyler(), parent=self)

    def _createConsoleApp(self):
        from qturtle.qtconsole import TranspylerConsole

        return TranspylerConsole(self.transpyler(), parent=self)

    def _createEditorApp(self):
        return TranspylerEditor(self.transpyler(), parent=self)

