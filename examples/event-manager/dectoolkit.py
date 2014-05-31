#!/usr/bin/python2.7

import sys

# utility functions
def args_to_str(args, kwargs):
    '''
    A string representation of an argument list.
    '''
    sep = ', '
    arglist = []
    if args:
        arglist.append(sep.join('{}'.format(arg) for arg in args))
    if kwargs:
        arglist.append(sep.join('{}={}'.format(*p) for p in kwargs.iteritems()))
    return sep.join(arglist)

# decorators
def decorate(target):
    '''
    Preserve the metadata of the decorated function.
    '''
    def decorator(func):
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)
        decorated.__name__ = target.__name__
        decorated.__doc__ = target.__doc__
        return decorated
    return decorator

def trace(func):
    '''
    Trace name, argument, and return value when a function is called.
    '''
    @decorate(func)
    def traced(*args, **kwargs):
        function = func.__name__
        arguments = args_to_str(args, kwargs)
        called = '{}({})'.format(function, arguments)
        returned = func(*args, **kwargs)
        sys.stderr.write(
            '<trace: called {} --> returned {}>\n'.format(called, returned)
            )
        return returned
    return traced
