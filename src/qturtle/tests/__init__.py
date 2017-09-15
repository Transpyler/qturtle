from PyQt5.QtWidgets import QWidget, QMenu, QAction


#
# Monkey Patching: improve widget's __repr__ to preserve our sanity ;)
#
QWidget.__repr__ = lambda x: '<%s: %s>' % (x.__class__.__name__, x._repr())
QWidget._repr = lambda x: '...'
QMenu._repr = lambda x: repr(x.title())
QAction.__repr__ = QWidget.__repr__
QAction._repr = lambda x: repr(x.text() or '...')