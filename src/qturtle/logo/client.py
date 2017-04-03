import sys
import time

from .connection import TCPConnection
from .core import function_description
from .cursor import CursorMessagesMixin, CursorManager
from .errors import InvalidResponseError
from .manager import Manager
from .utils import public, is_public


class GlobalMessagesMixin:
    """
    Public global functions.
    """

    @public
    def reset(self):
        """
        Clear all elements on the screen and put turtle black to the
        default state.
        """

        return {'action': 'reset'}

    @public
    def clear(self):
        """
        Clear all elements on the screen, but preserves turtle state.
        """

        return {'action': 'clear'}


class ClientBase:
    """
    Client base features. Do not include cursor and public API.
    """

    connection_factory = TCPConnection
    manager_factory = Manager
    cursor_factory = CursorManager

    def __init__(self, manager=None, connection=None):
        self.manager = manager or self.manager_factory()
        self.connection = connection or self.connection_factory(self.manager)

    def start(self):
        """
        Starts client.
        """

        self.manager.start()
        self.connection.start()

    def send_message(self, msg):
        """
        Sends a message through the default conection.
        """

        reply = self.connection.send(msg)
        return self.process_response(reply)

    def process_response(self, response):
        """
        Process message response.
        """

        status = response.get('status', None)
        if status == 'error':
            raise self.reconstruct_exception(response)
        elif status == 'result':
            return response.get('value')
        elif status == 'ok':
            return None
        else:
            raise InvalidResponseError('invalid response: %r' % response)

    def reconstruct_exception(self, response):
        """
        Create an exception from error message.
        """

        if response['status'] != 'error':
            raise InvalidResponseError(response)

        # Get class
        full_name = response.get('error', 'builtins.Exception')
        modname, name = full_name.rpartition('.')
        mod = __import__(modname, fromlist=[name])
        cls = getattr(mod, name)
        args = response.get('args', [])
        kwargs = response.get('kwargs', {})
        return cls(*args, **kwargs)

    def sleep(self, interval):
        """
        Sleeps during the given interval.
        """

        time.sleep(interval)

    def help_string(self):
        """
        Return a help message of all turtle functions.
        """

        L = ["List of supported turtle functions.\n"]
        for name, method in sorted(self.namespace().items()):
            try:
                if callable(method):
                    L.append(function_description(method))
            except AttributeError:
                pass
        return '\n\n'.join(L)

    def namespace(self):
        """
        Return a dictionary with the public namespace for client.
        """

        namespace = {}
        for funcname in dir(self):
            func = getattr(self, funcname)
            if is_public(func):
                namespace[funcname] = func
        return namespace

    def inject_namespace(self, globals=None):
        """
        Inject all namespace functions into the callee globals
        """

        if globals is None:
            frame = sys._getframe()
            frame = frame.f_back
            globals = frame.f_globals
        globals.update(self.namespace())


class Client(CursorMessagesMixin, GlobalMessagesMixin, ClientBase):
    """
    Default client class.
    """
