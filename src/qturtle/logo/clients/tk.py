from qturtle.logo.client import Client
from qturtle.logo.connection import InProcessConnection
from qturtle.logo.manager import InProcessManager
from qturtle.logo.server import TurtleServer


class TurtleClient(Client):
    """
    A client based on Python's builtin turtle module.
    """

    server_factory = TurtleServer
    connection_factory = InProcessConnection
    manager_factory = InProcessManager

    def __init__(self, **kwargs):
        server = self.server_factory()
        manager = self.manager_factory(server=server)
        super().__init__(manager=manager, **kwargs)
        self.server = server


if __name__ == '__main__':
    t = TurtleClient()
    t.start()
    t.inject_namespace(globals())

    print(t.namespace().keys())

    for _ in range(12):
        forward(200)
        left(5 * 360 / 12)
    t.sleep(2)
