from functools import wraps as _wraps
from .mathutils import Vec as _Vec


def vecargsmethod(func):
    """
    Decorates a function of a vec object to accept the following signatures:

        func(vec, **kwds)
        func(x, y, **kwds)

    A Vec object is always passed to the given implementation.
    """

    @_wraps(func)
    def decorated(self, x, y=None, **kwds):
        if y is None:
            try:
                x, y = x
            except ValueError:
                raise ValueError('expected 2 elements, got %s' % len(x))

            return func(self, _Vec(x, y), **kwds)
        else:
            return func(self, _Vec(x, y), **kwds)

    return decorated


def alias(*args):
    """
    Set a list of function aliases for TurtleFunction methods.

    The aliases are automatically included in the resulting namespace.
    """

    def decorator(func):
        func.alias_list = args
        return func

    return decorator


def public(func):
    """
    Mark function as public.
    """

    func._is_pylogo_public = True

    @_wraps(func)
    def decorated(self, *args, **kwargs):
        from .cursor import CursorManager

        msg = func(self, *args, **kwargs)
        if isinstance(self, CursorManager):
            msg['cursor-id'] = self._id
            return self._client.send(msg)
        else:
            return self.send_message(msg)

    return decorated


def is_public(func):
    """
    Return True for functions marked with the @public decorator.
    """

    return getattr(func, '_is_pylogo_public', False)



def object_ctrl(getter, setter=None):
    def fget(self):
        return getattr(self.object, getter)()

    if setter is not None:
        def fset(self, value):
            getattr(self.object, setter)(value)

        return property(fget, fset)
    else:
        return property(fget)