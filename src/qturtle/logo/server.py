from .errors import InvalidMessageError
from .cursor import Cursor, TurtleCursor


class Server:
    """
    Server base class.
    """

    cursor_factory = Cursor

    def __init__(self):
        self.cursors = {}
        self._cursor_idx = 0

    def new_cursor(self, **kwargs):
        """
        Create a new cursor and add to the cursors list.
        """

        new = self.cursor_factory(self, self._cursor_idx, **kwargs)
        self._cursor_idx += 1
        return new

    def start(self):
        """
        Start server.
        """

        self.start_cursors()

    def start_cursors(self):
        """
        Initialize list of cursors.
        """

        cursor = self.new_cursor()
        self.cursors[cursor.id] = cursor

    def dispatch_message(self, message):
        """
        Dispatch message to the appropriate method.
        """

        action = message['action']
        idx = message.get('cursor-id', None)
        try:
            method = getattr(self, 'process_' + action.replace('-', '_'))
        except AttributeError:
            raise InvalidMessageError(message)
        else:
            args = message.get('args', ())
            kwargs = message.get('kwargs', {})
            if idx is not None:
                kwargs['idx'] = idx
            return method(*args, **kwargs)

    def process_set_state(self, state, value, idx=0):
        self.cursors[idx].set_state(state, value)

    def process_get_state(self, state, idx=0):
        return self.cursors[idx].get_state(state)

    def process_draw(self, pos, idx=0):
        self.cursors[idx].draw(pos)

    def process_step(self, step, idx=0):
        self.cursors[0].forward(step)

    def process_rotate(self, angle, idx=0):
        self.cursors[0].rotate(angle)


class InProcessServer(Server):
    """
    Base class for servers that share the same process as client.
    """


class TurtleServer(InProcessServer):
    """
    A server based on Python's builtin turtle module.
    """

    def __init__(self):
        super().__init__()

        # Init turtle module
        import turtle
        self._turtle = turtle

    def start(self):
        self._turtle.showturtle()
        super().start()

    def start_cursors(self):
        turtle = self._turtle.turtles()[0]
        self.cursors[0] = TurtleCursor(self, 0, turtle)
