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
