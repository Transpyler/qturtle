import os
import pytest
from qturtle.mixins import ToggleThemeMixin
from qturtle.mixins import ReplElementMixin

'''
Tests for the ToggleThemeMixin class
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
Tests for the ReplElementMixin class
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
    assert result == result
