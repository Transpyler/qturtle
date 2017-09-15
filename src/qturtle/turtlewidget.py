from PyQt5 import QtWidgets
from lazyutils import delegate_to

from .repleditor import ReplEditor
from .turtlescene import TurtleScene, TurtleView


class TurtleWidget(QtWidgets.QWidget):
    """
    Main widget of application: it has a GraphicsScene and a ReplEditor
    components. The full application simply wraps this widget inside a window
    with some menus.
    """

    zoomIn = delegate_to('_view')
    zoomOut = delegate_to('_view')
    saveImage = delegate_to('_view')
    flushExecution = delegate_to('_scene')
    increaseFont = delegate_to('_repl_editor')
    decreaseFont = delegate_to('_repl_editor')
    toggleTheme = delegate_to('_repl_editor')
    text = delegate_to('_repl_editor')
    setText = delegate_to('_repl_editor')

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
        self._repl_editor = ReplEditor(header_text=header_text,
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
        self._scene.messageReplySignal.connect(
            self._repl_editor.handleMessageReply)

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
