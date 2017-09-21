import warnings

from PyQt5 import QtCore


class ToggleThemeMixin:
    """
    Base class for objects that can toggle the dark/light themes.
    """

    def __init__(self, theme='dark', **kwargs):
        self._theme = theme
        super().__init__(**kwargs)

    def toggleTheme(self):
        if self._theme == 'dark':
            self.setTheme('light')
        else:
            self.setTheme('dark')

    def theme(self):
        return self._theme

    def setTheme(self, name):
        self._theme = name


class ReplElementMixin(ToggleThemeMixin):
    """
    Base class for Editor and Console.
    """

    def widget(self):
        return self


class TranspylerEditorMixin(ReplElementMixin):
    """
    Base functionality to all Editor implementations.
    """

    def setConsole(self, console):
        self._console = console

    def runCode(self):
        """
        Runs the source code in the editor when user press Control + Return
        """

        if not hasattr(self, '_console'):
            raise RuntimeError('no console was set to editor!')
        self._console.runCode(self.fullText())

    def fullText(self):
        """
        Return the full text contents of editor.
        """
        raise NotImplementedError


class TranspylerConsoleMixin(ReplElementMixin):
    """
    Base console class.
    """

    printToConsoleSignal = QtCore.pyqtSignal(str, bool)

    def __init__(self,
                 transpyler,
                 parent=None, *,
                 header_text=None,
                 theme='dark',
                 hide_margins=True,
                 scene_handler=None, **kwargs):
        self._transpyler = transpyler
        self._header_text = header_text
        self._hide_margins = hide_margins
        self._scene_handler = scene_handler
        super().__init__(theme=theme, parent=parent, **kwargs)

    transpyler = lambda self: self._transpyler
    sceneHandler = lambda self: self._scene_handler

    def updateScene(self, call, turtle=None):
        handler = self._scene_handler
        if handler is None:
            print('msg:', call, ' turtle:', turtle)
            warnings.warn('must set the sceneHandler to handle this message')
        else:
            handler(call, turtle)

    def setSceneHandler(self, handler):
        self._scene_handler = handler

    def setNamespace(self, value):
        """
        Sets console namespace.
        """
        raise NotImplementedError

    def contextMenuEvent(self, e):
        pass

    def runCode(self, text):
        """
        Run code on terminal.
        """

        raise NotImplementedError
