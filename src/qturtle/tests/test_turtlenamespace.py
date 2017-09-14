'''

OBS:
Every function that had any think related with the atribute scene could not be tested,
 because the class TurtleScene give seg. fault when it is instaciated
'''

import sys
import pytest
import mock

from PyQt5 import QtWidgets
from qturtle.turtlenamespace import TurtleNamespaceEnglish, TurtleNamespace
from transpyler.turtle.qt.scene import TurtleScene 

 # TurtleNamespaceEnglish tests

@pytest.fixture
def  turtle_namespace_english():
    return TurtleNamespaceEnglish(scene='test');

def test_init_(turtle_namespace_english):
    assert isinstance(turtle_namespace_english,TurtleNamespaceEnglish)
    assert turtle_namespace_english._blacklist == set(turtle_namespace_english._BLACKLIST) 
    assert turtle_namespace_english._delay == 0.05 

def test__delitem__(turtle_namespace_english):
    assert turtle_namespace_english._data['back'] != None
    turtle_namespace_english.__delitem__('back')
    try:
        assert turtle_namespace_english._data['back']
        assert False
    except KeyError:
        assert True

def test__getitem__(turtle_namespace_english):
    assert turtle_namespace_english._data['back'] == turtle_namespace_english.__getitem__('back')

def test__setitem__(turtle_namespace_english):
    turtle_namespace_english.__setitem__('test',1)

'''
def test__iter__(turtle_namespace_english):
    assert turtle_namespace_english.__iter__() == iter(turtle_namespace_english._data)
'''
def test__len__(turtle_namespace_english):
    assert turtle_namespace_english.__len__() == len(turtle_namespace_english._data)

def test__getaliases(turtle_namespace_english):
    assert turtle_namespace_english._getaliases() == {'back': 'backward',\
                                                        'bk': 'backward',\
                                                        'fd': 'forward',\
                                                        'lt': 'left',\
                                                        'pd': 'pendown',\
                                                        'pu': 'penup',\
                                                        'rt':'right'}

def test_blacklist(turtle_namespace_english):
   turtle_namespace_english.blacklist('test')
   assert 'test' in turtle_namespace_english._blacklist

def test_speed(turtle_namespace_english):
    assert turtle_namespace_english._delay == 0.05
    turtle_namespace_english.speed(5)
    assert turtle_namespace_english._delay  == max(0.05/5**2 - 0.0005, 0)
    

# TurtleNamespace tests
'''
@pytest.fixture
def turtle_namespace():
    return TurtleNamespace('test')

def test_frente(turtle_namespace):
turtle_namespace.frente(5) 
'''

# Other functions
def test_helpstr():
    import io
    import qturtle.turtlenamespace as turtle_namespace
    stdout, sys.stdout = sys.stdout, io.StringIO()
    help('def')
    assert turtle_namespace.helpstr('def') == sys.stdout.getvalue()
