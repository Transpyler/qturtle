#
# Monkey patch QtLogging
#
import pytest
from pytestqt.qt_compat import qt_api

from qturtle.mainwindow import TurtleMainWindow


def monkey_patched_record():
    from pytestqt.logging import Record

    def _get_msg_type_name(cls, msg_type):
        if not getattr(cls, '_type_name_map', None):
            cls._type_name_map = {
                qt_api.QtDebugMsg: 'QtDebugMsg',
                qt_api.QtWarningMsg: 'QtWarningMsg',
                qt_api.QtCriticalMsg: 'QtCriticalMsg',
                qt_api.QtFatalMsg: 'QtFatalMsg',
            }
        return cls._type_name_map.get(msg_type, 'QtErrorMsg')

    def _get_log_type_name(cls, msg_type):
        if not getattr(cls, '_log_type_name_map', None):
            cls._log_type_name_map = {
                qt_api.QtDebugMsg: 'DEBUG',
                qt_api.QtWarningMsg: 'WARNING',
                qt_api.QtCriticalMsg: 'CRITICAL',
                qt_api.QtFatalMsg: 'FATAL',
            }
        return cls._log_type_name_map.get(msg_type, 'ERROR')

    Record._get_msg_type_name = classmethod(_get_msg_type_name)
    Record._get_log_type_name = classmethod(_get_log_type_name)


@pytest.fixture
def main_window(qtbot):
    widget = TurtleMainWindow()
    qtbot.addWidget(widget)
    return widget


monkey_patched_record()
