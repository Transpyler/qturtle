from PyQt5 import QtWidgets
from lazyutils import delegate_to

from .turtlescene import TurtleScene, TurtleView
from .qsci.qscirepleditor import QsciReplEditor


class TurtleWidget(QtWidgets.QWidget):
    """
    Main widget of application: it has a GraphicsScene and a ReplEditor
    components. The full application simply wraps this widget inside a window
    with some menus.
    """

    text = delegate_to('_editor')
    setText = delegate_to('_editor')
    zoomIn = delegate_to('_view')
    zoomOut = delegate_to('_view')
    increaseFont = delegate_to('_editor')
    decreaseFont = delegate_to('_editor')
    toggleTheme = delegate_to('_editor')
    saveImage = delegate_to('_view')
    flushExecution = delegate_to('_scene')

    def __init__(self,
                 transpyler,
                 parent=None,
                 text='', header_text=None, **kwds):
        super().__init__(parent=parent)
        assert transpyler

        # Configure scene
        self._scene = TurtleScene()
        self._view = TurtleView(self._scene)

        # Configure editor
        self._transpyler = transpyler
        self._repl_editor = QsciReplEditor(header_text=header_text,
                                           transpyler=transpyler)
        self._repl_editor.setText(text)
        self._repl_editor.initNamespace()
        self._repl_editor.sizePolicy().setHorizontalPolicy(7)

        # Configure layout
        self._splitter = QtWidgets.QSplitter()
        self._splitter.addWidget(self._view)
        self._splitter.addWidget(self._repl_editor)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._splitter)
        self._splitter.setSizes([200, 120])

        # Connect signals
        self._repl_editor.turtleMessageSignal.connect(self._scene.handleMessage)
        self._scene.messageReplySignal.connect(self._repl_editor.handleMessageReply)

    def scene(self):
        return self._scene

    def view(self):
        return self._view

    def namespace(self):
        return self._namespace

    def replEditor(self):
        return self._repl_editor

    def fontZoomIn(self):
        self._repl_editor.zoomIn()

    def fontZoomOut(self):
        self._repl_editor.zoomOut()

    def fontZoomTo(self, factor):
        self._repl_editor.zoomTo(factor)

    def toggleTheme(self):
        self._repl_editor.toggleTheme()

    def text(self):
        return self._repl_editor.text()

    def setText(self, text):
        self._repl_editor.setText(text)