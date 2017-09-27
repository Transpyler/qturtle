import os
import pytest
from qturtle.mixins import ToggleThemeMixin
from qturtle.mixins import ReplElementMixin
from qturtle.mixins import TranspylerEditorMixin
from qturtle.mixins import TranspylerConsoleMixin
import warnings

'''
Tests of the ToggleThemeMixin class
'''
@pytest.fixture
def mixins():
    variable = ToggleThemeMixin()
    variable._theme = 'dark'
    return variable

@pytest.fixture
def name():
    return 'light'

def test_toggletheme(mixins):
    mixins.toggleTheme()
    result = mixins.theme()
    assert result == 'light'

def test_togglethemeLight(mixins):
    mixins.setTheme('light')
    mixins.toggleTheme()
    result = mixins.theme()
    assert result == 'dark'

def test_theme(mixins):
    result = mixins.theme()
    assert result == 'dark'

def test_setTheme(mixins,name):
    mixins.setTheme(name)
    result = mixins.theme()
    assert result == 'light'

'''
Tests of the ReplElementMixin class
'''
@pytest.fixture
def repmixin():
    variable = ReplElementMixin()
    return variable

'''
Research a better implementation for the test bellow
'''
def test_widget(repmixin):
    result = repmixin.widget()
    assert result == repmixin

'''
Tests of the TranspylerEditorMixin class
'''
@pytest.fixture
def editorMixin():
    variable = TranspylerEditorMixin()
    variable._console = 'console'
    return variable

@pytest.fixture
def console():
    return 'test_console'

def test_setConsole(editorMixin,console):
    result = editorMixin
    result.setConsole(console)
    assert result._console == 'test_console'

def test_fullText(editorMixin):
    with pytest.raises(NotImplementedError):
        editorMixin.fullText()

def test_runCodeHasNotattr(editorMixin):
    result = editorMixin
    result.setConsole(None)
    if not hasattr(editorMixin,'_console'):
        with pytest.raises(RuntimeError):
            result.runCode()

def test_runCodeHasattr(editorMixin):
    result = editorMixin
    with pytest.raises(NotImplementedError):
        result.fullText()

'''
Tests of the TranspylerConsoleMixin class
'''
'''
@pytest.fixture
def consoleMixin():
    transpyler = "test"
    variable = TranspylerConsoleMixin()
    variable._transpyler = transpyler
    variable._scene_handler = None
    return variable

@pytest.fixture
def call():
    return 'test'

@pytest.fixture
def turtle():
    return None

def test_setNamespace(consoleMixin,value):
    result = consoleMixin
    with pytest.raises(NotImplementedError):
        result.setNamespace(value)
'''
