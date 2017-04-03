import pytest
from PyQt5 import QtCore
import mock
from qturtle.mainwindow import TurtleMainWindow


@pytest.yield_fixture
def main_window(qtbot):
    widget = TurtleMainWindow()
    qtbot.addWidget(widget)
    with mock.patch('qturtle.qsci.qsciconsole.TranspylerConsole.timerEvent',
                    lambda x, t: None):
        yield widget


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
