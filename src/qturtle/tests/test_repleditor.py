import sys
import pytest
from qturtle.qsci.qscirepleditor import QsciReplEditor
from qturtle.qsci.qsciconsole import TranspylerConsole
from transpyler import Transpyler
from PyQt5 import QtWidgets

@pytest.fixture
def m_transpyler():
    trans = Transpyler()
    return trans

@pytest.fixture
def repleditor(m_transpyler):
    app = QtWidgets.QApplication(sys.argv)
    return QsciReplEditor(m_transpyler)

def test_handleMessageReply(repleditor):
    pass


