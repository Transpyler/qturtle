from PyQt5 import QtWidgets, QtCore

from .mixins import ToggleThemeMixin
from .qscieditor import TranspylerEditor
from .qtconsole import TranspylerConsole


class ReplEditor(ToggleThemeMixin, QtWidgets.QWidget):
    """
    A Widget with a foldable editor part and a REPL console.

    The editor and the console are layed out vertically and users can fold it
    in order to either hide the editor, the console or to show both
    simultaneously.
    """

    @property
    def turtleMessageSignal(self):
        return self._console.turtleMessageSignal

    def __init__(self,
                 transpyler,
                 parent=None, *,
                 theme='dark',
                 header_text=None,
                 hide_console_margins=False):
        assert transpyler
        super().__init__(parent=parent, theme=theme)
        self._transpyler = transpyler
        self._header_text = header_text
        self._hide_console_margins = hide_console_margins
        self._console = self._createConsoleApp()
        self._editor = self._createEditorApp()
        self._editor.setConsole(self._console)

        # Create buttons
        run_button = QtWidgets.QPushButton('Run')
        hideup_button = QtWidgets.QPushButton('\u25b2')
        hidedown_button = QtWidgets.QPushButton('\u25bc')
        run_button.setMaximumWidth(100)
        hideup_button.setFixedWidth(35)
        hidedown_button.setFixedWidth(35)
        buttons = QtWidgets.QWidget()
        button_area = QtWidgets.QHBoxLayout(buttons)
        button_area.addWidget(hideup_button, 20)
        button_area.addWidget(hidedown_button, 20)
        button_area.addStretch(300)
        button_area.addWidget(run_button, 200)
        button_area.setContentsMargins(0, 0, 0, 0)
        buttons.setFixedHeight(25)

        # Connect signals
        run_button.clicked.connect(self.runEditorCode)
        hideup_button.clicked.connect(self.hideUp)
        hidedown_button.clicked.connect(self.hideDown)

        # Create top area with the Editor and the button area element
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._editor.widget())
        top_layout.addWidget(buttons)
        self._top_widget = top_widget

        # Add elements
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation(0))
        splitter.addWidget(top_widget)
        splitter.addWidget(self._console.widget())
        splitter.setSizes([200, 120])
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self._splitter = splitter
        self._splitter_sizes = splitter.sizes()

        # Size hints
        self.setMinimumSize(QtCore.QSize(100, 200))

        # Set theme
        self.setTheme(self.theme())

    def handleMessageReply(self, msg):
        self._console.handleMessageReply(msg)

    def transpyler(self):
        return self._transpyler

    def console(self):
        return self._console

    def editor(self):
        return self._editor

    def sizeHint(self):
        return QtCore.QSize(100, 200)

    def setNamespace(self, ns):
        self._console.setNamespace(ns)

    def initNamespace(self):
        self._console.initNamespace()

    def runEditorCode(self):
        text = self._editor.fullText()
        if text:
            result = self._console.runCode(text)
            if result and self._console.isHidden():
                self.toggleConsoleVisibility()

    def toggleConsoleVisibility(self):
        if self._console.isHidden():
            self._console.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([2 ** 16, 1])
            self._console.setHidden(True)

    def toggleEditorVisibility(self):
        if self._editor.isHidden():
            self._editor.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([1, 2 ** 16])
            self._editor.setHidden(True)

    def hideUp(self):
        if self._console.isHidden():
            self.toggleConsoleVisibility()
        elif not self._editor.isHidden():
            self.toggleEditorVisibility()

    def hideDown(self):
        if self._editor.isHidden():
            self.toggleEditorVisibility()
        elif not self._console.isHidden():
            self.toggleConsoleVisibility()

    def setText(self, text):
        self._editor.setText(text)

    def text(self):
        return self._editor.text()

    def setTheme(self, theme):
        self._console.setTheme(theme)
        self._editor.setTheme(theme)

    def zoomIn(self):
        self._console.zoomIn()
        self._editor.zoomIn()

    def zoomOut(self):
        self._console.zoomOut()
        self._editor.zoomOut()

    def zoomTo(self, factor):
        self._console.zoomTo(factor)
        self._editor.zoomTo(factor)

    def _createConsoleApp(self):
        return TranspylerConsole(self.transpyler(), parent=self)

    def _createEditorApp(self):
        return TranspylerEditor(self.transpyler(), parent=self)
