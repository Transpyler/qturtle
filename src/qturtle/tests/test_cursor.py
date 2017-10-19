import pytest
import mock
from qturtle.logo.cursor import Cursor, TurtleCursor
from qturtle.logo.mathutils import Vec 

@pytest.fixture
def cursor():
    return Cursor(server=None,id=0, pos=None, heading=0.0, drawing=True, \
                 color='black', fillcolor='black', width=1, hidden=False)

def test__init__(cursor):
    assert isinstance(cursor,Cursor)
    assert cursor.server == None
    assert cursor.id == 0
    assert cursor.pos == cursor.vec(None or (0, 0))
    cursor.heading == 0.0
    cursor.is_drawing = True 
    cursor.color == 'black'
    cursor.fillcolor == 'black'
    cursor.width == 1
    cursor.hidden == False 

def test_rotate(cursor):
    cursor.heading == 0.0
    cursor.rotate(1)
    assert cursor.heading == 1.0

def test_step(cursor):
    cursor.pos == Vec(0.0, 0.0)
    cursor.step(5)
    assert cursor.pos == Vec(5.0, 0.0)

def test_get_set_state_wrong(cursor):
   cursor.set_state('pos','test')
   assert cursor.get_state('pos') == 'test'
   
def test_get_state_wrong(cursor):
    try:
        assert cursor.get_state(None) == None
        assert False

    except ValueError:
        assert True

def test_set_state_wrong(cursor):
    try:
        assert cursor.set_state(None,'') == None
        assert False

    except ValueError:
        assert True


@pytest.fixture
def turtle_cursor(cursor):
    test_mock = mock.MagicMock()
    test_mock.is_drawing.return_value = False
    test_mock.pos.return_value = Vec(0.0, 0.0)
    return TurtleCursor(None,0,test_mock)
        
def test_turtle_cursor_init(turtle_cursor):
    assert isinstance(turtle_cursor,TurtleCursor)
