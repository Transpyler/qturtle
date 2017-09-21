import uuid
from collections import deque
from logging import getLogger

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from jupyter_client.localinterfaces import is_local_ip
from lazyutils import lazy
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

from transpyler import Transpyler
from transpyler.jupyter.app import TranspylerKernelManager
from transpyler.jupyter.setup import setup_assets
from qturtle import colors
from qturtle.mixins import TranspylerConsoleMixin

from .styles import dark_style_sheet, dark_syntax_style, dark_style_template

log = getLogger('gui.ipytuga')
_ = lambda x: x


class ITranspylerQtConsoleApp(JupyterQtConsoleApp):
    """
    Subclass of JupyterQtConsoleApp that initializes a pytuga kernel instead of
    a regular python kernel.
    """

    transpyler = None
    theme = 'dark'
    banner = _('Welcome to QTurtle!')

    @lazy
    def use_kernel(self):
        return self.transpyler.name or 'python'

    def __init__(self, *args, transpyler=None, **kwargs):
        super().__init__(*args, **kwargs)
        if transpyler is not None:
            self.transpyler = transpyler
        self.use_kernel = kwargs.pop('use_kernel', self.use_kernel)

    def init_kernel_client(self):
        super().init_kernel_client()
        self.shell_channel = self.kernel_client.shell_channel

    def initialize(self, argv=None):
        from jupyter_client.kernelspec import NoSuchKernel

        argv = ['--kernel', self.use_kernel]
        transpyler = self.transpyler
        try:
            return super().initialize(argv)
        except NoSuchKernel:
            script_path = TranspylerKernelManager.kernel_script_path
            self.kernel_manager.kernel_script_path = script_path
            self.kernel_manager.transpyler = transpyler
            self.kernel_manager.name = transpyler.name
            setup_assets(transpyler, user=True)
            return super().initialize(argv)

    def execute(self, code, silent=True, **kwargs):
        """
        Sends command to interpreter.
        """

        return self.kernel_client.execute(code, silent=silent, **kwargs)

    def toggle_theme(self):
        """
        Toggles between dark/light themes.
        """

        if self.theme == 'dark':
            self.set_theme('light')
        else:
            self.set_theme('dark')

    def set_theme(self, theme):
        if theme == 'dark':
            self.widget.style_sheet = dark_style_sheet
            self.widget.syntax_style = dark_syntax_style
        elif theme == 'light':
            self.widget.set_default_style('lightbg')
        else:
            raise ValueError('invalid theme: %r' % theme)
        self.theme = theme


