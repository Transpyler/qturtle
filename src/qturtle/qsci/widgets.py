class JupyterRichTextEditor(RichJupyterWidget):
    def __init__(self, app, transpyler, parent=None):
        self.app = app
        self.transpyler = transpyler
        super().__init__(
            parent=parent,
            config=app.config,
            local_kernel=(not app.existing) or is_local_ip(app.ip),
            gui_completion='droplist',
            in_prompt='',
        )

        self.style_sheet = styles.default_dark_style_sheet
        self.syntax_style = styles.default_dark_syntax_style
        self._existing = app.existing
        self._may_close = not app.existing
        self._confirm_exit = app.confirm_exit
        self._display_banner = False
        self.kernel_manager = app.kernel_manager
        self.kernel_client = app.kernel_client

    def toggleTheme(self):
        pass


class QutepartTranspylerEditor(Qutepart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_defaults()

    def __set_defaults(self):


    def setText(self, text):
        del self.lines[:]
        for line in text.splitlines():
            self.lines.append(line)
