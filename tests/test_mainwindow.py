import os

import mock
import pytest

pytestmark = [
    pytest.mark.skipif(os.environ.get('TEST_QT', 'true') == 'false',
                       reason='disable QT on CI until we figure out how to do it ;)')
]


@pytest.fixture
def menus(main_window):
    btn, *menu_list = main_window.menuBar.children()
    menu_map = {}
    for menu in menu_list:
        name = menu.objectName()[4:].lower()
        menu_map[name] = menu
    return menu_map


class TestClickMenus:
    def test_can_click_all_editor_menus(self, menus):
        actions = menus['editor'].actions()
        for action in actions:
            action.triggered.emit()

    def test_can_click_all_canvas_menus(self, menus):
        for action in menus['canvas'].actions():
            action.triggered.emit()

    def test_examples(self, menus, main_window):
        last_text = None
        for action in menus['examples'].actions()[:-1]:
            action.triggered.emit()
            text = main_window.editorText()
            assert text != last_text
            main_window.setEditorText(text)

    def test_help_menu(self, menus):
        docs, about, _, update = menus['help'].actions()

        def func(w, title, msg):
            assert title == 'Pytuguês'

        with mock.patch('PyQt5.QtWidgets.QMessageBox.about', func):
            about.triggered.emit()
