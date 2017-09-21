from logging import getLogger

from PyQt5 import QtWidgets
from jupyter_client.localinterfaces import is_local_ip
from lazyutils import lazy


from .styles import dark_style_sheet, dark_syntax_style
from .itranspyler_qt_consoleapp import ITranspylerQtConsoleApp

log = getLogger('gui.ipytuga')
_ = lambda x: x


class ITranspylerWidgetQtConsoleApp(ITranspylerQtConsoleApp):
    """
    A simplified application that exposes only a simple terminal widget instead
    of a full application with menus. This is useful for embeding in other
    applications.
    """

    @lazy
    def parent_widget(self):
        return QtWidgets.QWidget()

    @lazy
    def window(self):
        return self.parent_widget.window()

    @lazy
    def widget(self):
        self.initialize()
        log.info('Pytuga kernel initialized with --kernel %s' % self.use_kernel)
        return self.widget

    def __init__(self, parent_widget=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent_widget

    def init_qt_app(self):
        self.app = None

    def init_qt_elements(self):
        ip = self.ip
        local_kernel = (not self.existing) or is_local_ip(ip)
        self.widget = widget = self.widget_factory(
            parent=self.parent_widget,
            config=self.config,
            local_kernel=local_kernel,
            banner='',
            kernel_banner='',
            gui_completion='droplist',
            in_prompt='>>>',
            out_prompt='-->',
        )
        widget.style_sheet = dark_style_sheet
        widget.syntax_style = dark_syntax_style
        widget._existing = self.existing
        widget._may_close = not self.existing
        widget._confirm_exit = self.confirm_exit
        widget._display_banner = self.display_banner
        widget.kernel_manager = self.kernel_manager
        widget.kernel_client = self.kernel_client

    def get_widget(self):
        return self.widget

    def start(self):
        pass

    def _handle_kernel_info_reply(self):
        pass
