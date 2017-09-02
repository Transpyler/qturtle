import sys
import os
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
    assert type(transpyler_console) == TranspylerConsole 

def test_getCurrentCommand(transpyler_console):
    assert transpyler_console.getCurrentCommand() == ''


def test_keyPressEvent_Return(transpyler_console):

    app = QtWidgets.QApplication(sys.argv)

    transpyler_console.isLocked = False
    transpyler_console._locked_position = (-1000,-1000)

    ev = mock.MagicMock()
    
    ev.key.return_value =  QtCore.Qt.Key_Return 
    transpyler_console.keyPressEvent(ev=ev)

    #ev.modifiers.return_value = False
    #transpyler_console.keyPressEvent(ev=ev)
