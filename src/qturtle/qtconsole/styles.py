'''
 Styles

 The default dark style sheet: white text on a black background.
'''

from qturtle import colors


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
