"""
These are functions that should be executed by the Kernel application.

In the language of the transpyler.tuga module, the GUI application is the turtle
server and the Jupyter kernel is the client. The forward(), left(),
etc functions on the client just send requests for the Qt application asking
for updates or information.
"""
from transpyler.turtle import state
from transpyler.turtle.qt.turtle import Turtle

TURTLES_COMM = None
MESSAGE_HANDLERS = []


class TurtleState(state.MirrorState):
    """
    A client state with fake inbox/outbox queues that redirects requests to
    the comm channnel.
    """

    _turtle_id = 0

    def __init__(self, *args, **kwargs):
        TurtleState._turtle_id += 1
        kwargs['id'] = self._turtle_id
        super().__init__(*args, **kwargs)

    def send(self, msg):
        TURTLES_COMM.send(msg)
        if msg[0] == 'newturtle':
            return ['newturtle', None]
        else:
            return [msg[0], self.id]


Turtle._state_factory = TurtleState


def handle_qturtle_comm(comm, msg):
    """
    Handles message using the specified comm object.

    The handler should return the reply message from the given input.
    """

    global TURTLES_COMM

    @comm.on_msg
    def recv(msg):
        data = msg['content']['data']
        for handler in MESSAGE_HANDLERS:
            handler(data)

    TURTLES_COMM = comm
    comm.send(['comm_open'])


def comm(ipython):
    """
    Register a handler for the comm object in the kernel.

    The application should now request a comm_open action for this comm.
    """
    ipython.kernel.comm_manager.register_target('turtles',
                                                handle_qturtle_comm)


def init_namespace(transpyler, ns):
    """
    Return the default namespace.
    """

    transpyler.qturtle = True
