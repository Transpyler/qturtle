"""
Code were adapted from qtconsole.qtconsoleapp to use Pytuga kernel.

This class create a Jupyter aplication which runs and interact with a Pytuga
kernel. The console app does not necessarely open a qt window. Use the
method .getWidget() or .showWidget() methods to initialize and show a qt widget
that interact the console application.
"""
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
from . import colors
from .mixins import TranspylerConsoleMixin

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


class TranspylerConsole(TranspylerConsoleMixin, QtWidgets.QWidget):
    """
    A Jupyter transpyler console that can be embedded in a ReplWidget.
    """

    printToConsoleSignal = QtCore.pyqtSignal(str, bool)
    turtleMessageSignal = QtCore.pyqtSignal(object)

    def __init__(self, transpyler, parent=None, **kwargs):
        super().__init__(transpyler=transpyler, parent=parent, **kwargs)
        self._app = ITranspylerWidgetQtConsoleApp(transpyler=transpyler)
        self._widget = self._app.widget
        self._turtle_mailbox_comm_id = None
        self._inbox_messages = deque()
        self._inbox_handlers = {}
        self._msg_handlers = {}
        self._app.kernel_client.iopub_channel.message_received.connect(
            self.messageEvent)

    def __del__(self):
        # Kills kernel when console is destroyed
        self._app.kernel_manager.shutdown_kernel(now=True)

    def initNamespace(self):
        if self._turtle_mailbox_comm_id is None:
            self.initTurtleComm()

        self.runCodeSilent(
            'from qturtle.kernel import init_namespace\n'
            'init_namespace(get_ipython().kernel.transpyler, globals())\n'
            'del init_namespace\n'
            'forward(0)  # create default turtle\n'
        )

    def initTurtleComm(self):
        """
        Create Comm link between Gui application and the kernel.
        """

        client = self._app.kernel_client

        # Register comm handler in the kernel
        self.runCodeSilent(
            'from qturtle.kernel import comm as _comm\n'
            '_comm(get_ipython())\n'
        )

        # Now sends a comm_open message through the shell channel. This
        # opens the handler and starts communication
        type = 'comm_open'
        self._turtle_mailbox_comm_id = str(uuid.uuid1())
        payload = {
            'comm_id': self._turtle_mailbox_comm_id, 'target_name': 'turtles'
        }
        msg = client.session.msg(type, payload)

        # The default handler in the kernel should send an acknowledge message.
        # We should listen to it in the iopub channel.
        def confirm_comm_open(msg):
            if msg != ['comm_open']:
                raise ValueError('got invalid response to comm_open: %s' % msg)

        msg_id = msg['header']['msg_id']
        self.registerMailboxHandler(msg_id, confirm_comm_open)
        client.shell_channel.send(msg)

    def messageEvent(self, msg):
        """
        Handles incomming messages in the comm channel.
        """

        msg_type = msg['msg_type']

        if msg_type == 'comm_msg':
            data = msg['content']['data']
            id = msg['parent_header']['msg_id']
            comm_id = msg['content']['comm_id']

            # Treat messages with registered handlers immediately
            if id in self._inbox_handlers:
                handler = self._inbox_handlers.pop(id)
                handler(data)
                return
            elif comm_id == self._turtle_mailbox_comm_id:
                data = msg['content']['data']
                self.turtleMessageSignal.emit(data)
            else:
                raise ValueError('invalid comm_id: %s' % data)

    def registerMailboxHandler(self, id, handler):
        """
        Register a callback for a message with the given id.
        """
        self._inbox_handlers[id] = handler

    def handleMessageReply(self, data):
        """
        Receives a message reply from the turtle server (usually the scene
        object). This reply should be sent back to the kernel using the open
        comm.
        """

        client = self._app.kernel_client
        payload = {
            'comm_id': self._turtle_mailbox_comm_id, 'data': data
        }
        msg = client.session.msg('comm_msg', payload)
        client.shell_channel.send(msg)

    def runCodeSilent(self, code):
        self._app.execute(code)

    def runCode(self, code):
        code = code.strip()
        if not code:
            return
        _ = self.transpyler().translate
        self._widget._show_prompt(_('Running code...'), newline=False)
        self._app.execute(code)
        self._widget.execute('')

    def setTheme(self, theme):
        self._app.set_theme(theme)

    def widget(self):
        return self._widget

    def _font_diff(self, diff):
        font = self._widget.font
        size = font.pointSize()
        font.setPointSize(size + diff)
        self._widget.font = font

    def zoomIn(self):
        self._font_diff(1)

    def zoomOut(self):
        self._font_diff(-1)

    def zoomTo(self, factor):
        font = self._widget.font
        font.setPointSize(10 + factor)
        self._widget.font = font


def start_qtconsole(transpyler=None, **kwargs):
    """
    Starts a transpyler-based qtconsole application.
    """

    transpyler = transpyler or Transpyler()
    kwargs['transpyler'] = transpyler
    ITranspylerQtConsoleApp.launch_instance(**kwargs)


# -----------------------------------------------------------------------------
# Styles
# -----------------------------------------------------------------------------

# The default dark style sheet: white text on a black background.
dark_style_template = '''
    QPlainTextEdit, QTextEdit {{
        background-color: {bgcolor};
        color: {fgcolor};
        selection-background-color: {bgselect};
    }}
    QFrame {{
        border: 1px solid grey;
    }}
    .error {{
        color: red;
    }}
    .in-prompt {{
        color: {prompt};
        font-weight: bold;
    }}
    .in-prompt-number {{
        color: {prompt_number};
        font-weight: bold;
    }}
    .out-prompt {{
        color: {prompt_out};
    }}
    .out-prompt-number {{
        color: {prompt_out_number};
        font-weight: bold;
    }}
    .inverted {{
        background-color: {fgcolor};
        color: {bgcolor};
    }}
'''
dark_style_sheet = dark_style_template.format(
    bgcolor=colors.COLOR_GRAY1,
    fgcolor='white',
    bgselect=colors.COLOR_GRAY2,
    prompt=colors.COLOR_BLUE_SEA,
    prompt_number=colors.COLOR_SALMON,
    prompt_out=colors.COLOR_SALMON_DARK,
    prompt_out_number=colors.COLOR_SALMON_DARK,
)
dark_syntax_style = 'monokai'

if __name__ == '__main__':
    start_qtconsole()
