"""
Code were adapted from qtconsole.qtconsoleapp to use Pytuga kernel.

This class create a Jupyter aplication which runs and interact with a Pytuga
kernel. The console app does not necessarely open a qt window. Use the
method .getWidget() or .showWidget() methods to initialize and show a qt widget
that interact the console application.

This module was refactor, and the classes of this module was transfered to qtconsole folder.
"""

from logging import getLogger

from qtconsole.qtconsoleapp import JupyterQtConsoleApp

from transpyler import Transpyler

###Qtconsole
from qtconsole.itranspyler_qt_consoleapp import ITranspylerQtConsoleApp
from qtconsole.styles import dark_style_sheet, dark_syntax_style, dark_style_template
from qtconsole.itranspyler_widget_qt_consoleapp import ITranspylerWidgetQtConsoleApp
from qtconsole.transpyler_console import TranspylerConsole
###


log = getLogger('gui.ipytuga')
_ = lambda x: x


def start_qtconsole(transpyler=None, **kwargs):
    """
    Starts a transpyler-based qtconsole application.
    """

    transpyler = transpyler or Transpyler()
    kwargs['transpyler'] = transpyler
    ITranspylerQtConsoleApp.launch_instance(**kwargs)

