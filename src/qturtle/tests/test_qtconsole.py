import os
import pytest
from PyQt5 import QtCore
import warnings
from transpyler import Transpyler
from lazyutils import lazy
from transpyler.jupyter.app import TranspylerKernelManager
from transpyler.jupyter.setup import setup_assets
from qturtle.qtconsole import ITranspylerQtConsoleApp
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

'''
Tests of the ITranspylerQtConsoleApp class
'''
class obj():
    def __init__(self,name="test"):
        super().__init__()
        self.name = name

@pytest.fixture
def qtConsole():
    ob = obj()
    variable = ITranspylerQtConsoleApp(transpyler=ob)
    return variable

def test_use_kernel(qtConsole):
    result = qtConsole.use_kernel
    assert result == "test"
