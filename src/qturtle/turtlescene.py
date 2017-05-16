from PyQt5 import QtCore
from transpyler.turtle.qt.scene import TurtleScene as _TurtleScene
from transpyler.turtle.qt.view import TurtleView

_turtle_view = TurtleView


class TurtleScene(_TurtleScene):
    """
    Adapts TurtleScene to use jupyter comms as IPC.
    """

    messageReplySignal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, fps=30):
        super().__init__(parent, fps, 'inbox', 'outbox')

    def timerEvent(self, timer):
        # We disable the default timer.
        # Messages are handled by registering the handleMessage handler to
        # the turtleMessageSignal of the jupyter console.
        pass

    def handleMessage(self, msg):
        reply = self._turtles.handle(msg)
        self.messageReplySignal.emit(reply)