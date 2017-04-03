from .utils import public, vecargsmethod, object_ctrl
from .mathutils import Vec
from . import mathutils


class Cursor:
    """
    A cursor (or turtle) represents a drawing element on screen.
    """

    valid_states = {'pos', 'heading', 'drawing', 'color', 'fillcolor', 'width'}

    @property
    def heading_direction(self):
        return Vec(self.cos(self.heading), self.sin(self.heading))

    def __init__(self, server, id, pos=None, heading=0.0, drawing=True,
                 color='black', fillcolor='black', width=1, hidden=False):
        self.server = server
        self.id = id
        self.pos = self.vec(pos or (0, 0))
        self.heading = heading
        self.is_drawing = drawing
        self.color = color
        self.fillcolor = fillcolor
        self.width = width
        self.hidden = hidden

    def rotate(self, angle):
        """
        Rotate cursor heading.
        """

        self.heading += angle

    def step(self, step):
        """
        Advance the given step in the direction of heading.
        """

        self.pos += self.heading_direction * step

    def get_state(self, state):
        """
        Get a state variable.
        """

        if state not in self.valid_states:
            raise ValueError('invalid state name: %r' % state)
        return getattr(self, 'state')

    def set_state(self, state, value):
        """
        Change value of a state variable.
        """

        if state not in self.valid_states:
            raise ValueError('invalid state name: %r' % state)
        return setattr(self, 'state', value)

    # Mathematical functions. We define them here so they can be overridable in
    # subclasses.
    cos = staticmethod(mathutils.cos)
    sin = staticmethod(mathutils.sin)
    tan = staticmethod(mathutils.tan)
    vec = staticmethod(mathutils.Vec)


class TurtleCursor(Cursor):
    """
    A cursor for Python's builtin turtle module.
    """

    heading = object_ctrl('heading', 'setheading')
    color = object_ctrl('pencolor', 'pencolor')
    fillcolor = object_ctrl('fillcolor', 'fillcolor')
    width = object_ctrl('width', 'width')
    pos = object_ctrl('pos')

    @pos.setter
    def pos(self, value):
        x, y = value
        is_drawing = self.is_drawing
        self.is_drawing = False
        self.object.goto(x, y)
        self.is_drawing = is_drawing

    is_drawing = object_ctrl('isdown')

    @is_drawing.setter
    def is_drawing(self, value):
        if value:
            self.object.pendown()
        else:
            self.object.penup()

    def __init__(self, server, id, object, **kwargs):
        self.object = object
        super().__init__(server, id, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.object, attr)

    def rotate(self, angle):
        if angle > 0:
            self.object.left(angle)
        else:
            self.object.right(-angle)

    def step(self, size):
        if size > 0:
            self.object.forward(size)
        elif size < 0:
            self.object.backward(-size)


class CursorMessagesMixin:
    """
    Public cursor functions.
    """

    # Speed control
    @public
    def speed(self, speed):
        """
        Set the simulation speed: its a number between 1 and 10, where
        0 is the slowest and 10 is the fastest.
        """

        return {'action': 'set-state', 'args': ['speed', speed]}

    # Direct state control
    @public
    def getpos(self):
        """
        Return a vector (x, y) with turtle's position (in pixels).
        """

        return {'action': 'get-state', 'args': ['pos']}

    @public
    @vecargsmethod
    def setpos(self, value):
        """
        Modifies turtle's position (in pixels)

        User can pass the x, y coordinates of the new position or a tuple of
        (x, y) values.
        """

        return {'action': 'set-state', 'args': ['pos', value]}

    @public
    def getheading(self):
        """
        Return current heading of the turtle (in degrees).
        """

        return {'action': 'get-state', 'args': ['heading']}

    @public
    def setheading(self, value):
        """
        Sets turtle's heading (in degrees).
        """

        return {'action': 'set-state', 'args': ['heading', value]}

    @public
    def getwidth(self):
        """
        Return the pen width (in pixels):
        """

        return {'action': 'get-state', 'args': ['width']}

    @public
    def setwidth(self, value):
        """
        Modifies the pen width (in pixels)
        """

        return {'action': 'set-state', 'args': ['width', value]}

    @public
    def getcolor(self):
        """
        Return a tuple of (R, G, B) with the current pen color.
        """

        return {'action': 'get-state', 'args': ['color']}

    @public
    def setcolor(self, value):
        """
        Modifies the pen color.

        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.
        """

        return {'action': 'set-state', 'args': ['color', value]}

    @public
    def getfillcolor(self):
        """
        Return a tuple of (R, G, B) with the current fill color.
        """

        return {'action': 'get-state', 'args': ['fillcolor']}

    @public
    def setfillcolor(self, value):
        """
        Modifies the fill color.

        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.
        """

        return {'action': 'set-state', 'args': ['fillcolor', value]}

    @public
    def penup(self):
        """
        Raises the turtle pen so it stops drawing.
        """

        return {'action': 'set-state', 'args': ['is_drawing', False]}

    @public
    def pendown(self):
        """
        Lower the turtle pen so it can draw in the screen.
        """

        return {'action': 'set-state', 'args': ['is_drawing', True]}

    @public
    def isdown(self):
        """
        Return True if the pen is down or False otherwise.
        """

        return {'action': 'get-state', 'args': ['is_drawing']}

    # Movement functions
    @vecargsmethod
    def goto(self, pos):
        """
        Goes to the given position.

        If the pen is down, it draws a line.
        """

        return {'action': 'set-state', 'args': ['goto', pos, None]}

    @vecargsmethod
    def jumpto(self, pos):
        """
        Goes to the given position without drawing.
        """

        return {'action': 'set-state', 'args': ['goto', pos, False]}

    @public
    def forward(self, step):
        """
        Move the turtle forward by the given step size (in pixels).
        """

        return {'action': 'step', 'args': [step]}

    @public
    def backward(self, step):
        """
        Move the turtle backward by the given step size (in pixels).
        """

        return {'action': 'step', 'args': [-step]}

    @public
    def left(self, angle):
        """
        Rotate the turtle counter-clockwise by the given angle.

        Negative angles produces clockwise rotation.
        """

        return {'action': 'rotate', 'args': [angle]}

    @public
    def right(self, angle):
        """
        Rotate the turtle clockwise by the given angle.

        Negative angles produces counter-clockwise rotation. Return final
        heading.
        """

        return {'action': 'rotate', 'args': [-angle]}


class CursorManagerBase:
    """
    Controls a cursor object in the server.
    """

    def __init__(self, client, id):
        self._client = client
        self._id = id


class CursorManager(CursorMessagesMixin, CursorManagerBase):
    """
    Default manager for cursor obects.
    """