from PyQt5 import QtWidgets, QtCore

from .qsciconsole import TranspylerConsole
from .qscieditor import TranspylerEditor


from ..repleditor import ReplEditor


class QsciReplEditor(ReplEditor):
    def _createConsoleWidget(self):
        return TranspylerConsole(self.transpyler(), parent=self)

    def _createEditorWidget(self):
        return TranspylerEditor(self.transpyler(), parent=self)

