"""
These are functions that should be executed by the Jupyter kernel application.
"""
from transpyler import Transpyler
from transpyler.turtle import state
from transpyler.turtle.qt import Turtle

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


def init_namespace(transpyler: Transpyler, ns):
    """
    Update the given namespace with function computed from the transpyler
    object.
    """

    transpyler.has_turtle_functions = True
    transpyler.turtle_backend = 'qt'
    ns.update(transpyler.recreate_namespace())
