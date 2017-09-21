import os
import pytest
from PyQt5 import QtCore
import mock
from qturtle.mainwindow import TurtleMainWindow
from transpyler import Transpyler

pytestmark = [
    pytest.mark.skipif(os.environ.get('TEST_QT', 'true') == 'false',
                       reason='disable QT on CI until we figure out how to do it ;)')
]


@pytest.fixture
def main_window(qtbot):
    widget = TurtleMainWindow()
    qtbot.addWidget(widget)
    return widget


@pytest.fixture
def menus(main_window):
    btn, *menu_list = main_window.menuBar.children()
    menu_map = {}
    for menu in menu_list:
        menu_map[menu.objectName().lower()[4:]] = menu
    return menu_map


def test_can_click_all_editor_menus(menus):
    for action in menus['editor'].actions():
        action.triggered.emit()


def test_can_click_all_canvas_menus(menus):
    for action in menus['canvas'].actions():
        action.triggered.emit()


def test_examples(menus, main_window):
    last_text = None
    for action in menus['examples'].actions()[:-1]:
        action.triggered.emit()
        text = main_window.editorText()
        assert text != last_text
        main_window.setEditorText(text)


def test_help_menu(menus, main_window):
    docs, about, _, update = menus['help'].actions()

    def func(w, title, msg):
        assert title == 'Pytuguês'

    with mock.patch('PyQt5.QtWidgets.QMessageBox.about', func):
        about.triggered.emit()

@pytest.fixture
def turtle():
    variable = TurtleMainWindow()
    variable._transpyler = 1
    variable._turtlewidget.setText("TEST")
    return variable

@pytest.fixture
def text():
    variable = "testText"
    return variable

def test_transpyler(turtle):
    result = turtle.transpyler()
    assert result == 1

def test__defaultTranspyler(turtle):
    result = turtle._defaultTranspyler()
    assert result == Transpyler()

def test_editorText(turtle):
    result = turtle.editorText()
    assert result == "TEST"

def test_setEditorText(turtle,text):
    turtle.setEditorText(text)
    result = turtle.editorText()
    assert result == "testText"
