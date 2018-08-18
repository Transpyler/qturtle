import sys
import pytest
import mock
from qturtle.qsci.qsciconsole import TranspylerConsole
from qturtle.qsci.runner import TranspylerRunner
from PyQt5 import QtCore, QtWidgets, QtGui
from transpyler import Transpyler
from qturtle.mainwindow import TurtleMainWindow
from qturtle.qsci.runner import TranspylerRunner


@pytest.fixture
def m_transpyler():
    trans = Transpyler()
    return trans

@pytest.fixture
def qt_widget():
    app = QtWidgets.QApplication(sys.argv)
    return app
    
@pytest.fixture
def transpyler_console(m_transpyler):

    app = QtWidgets.QApplication(sys.argv)
    return TranspylerConsole(m_transpyler)

def test__init__(transpyler_console):
    assert isinstance(transpyler_console,TranspylerConsole) 

def test_getCurrentCommand(transpyler_console):
    assert transpyler_console.getCurrentCommand() == ''
    transpyler_console._current_command = 'test'
    assert transpyler_console.getCurrentCommand() == 't\ne\ns\nt\n'

'''
def test_inputDialog(qtbot, transpyler_console):
    import _thread
    import time, random 

    app = QtWidgets.QApplication(sys.argv)
    with qtbot.waitSignals( transpyler_console.inputDialog('test')):
        qtbot.addWidget(input_dialog)
        assert qtbot.waitForWindowShown(inputDialog)

def test_keyPressEvent_Return(transpyler_console):
    from collections import deque 
    app = QtWidgets.QApplication(sys.argv)

    #transpyler_console.isLocked = False
    #transpyler_console._locked_position = (-1000,-1000)

    ev = mock.MagicMock()
    
    transpyler_console.background_tasks = deque(True)
    ev.key.return_value =  QtCore.Qt.Key_Escape
    transpyler_console.keyPressEvent(ev=ev)
'''
