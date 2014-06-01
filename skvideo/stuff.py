#
# A sample file
#

__all__ = ['do_something']

import fortran_stuff

def do_something(x):
    """
    Routine that does something

    Parameters
    ----------
    x : object
        Some input parameter
    
    Returns
    -------
    y : array
        Some relevant integers

    Notes
    -----
    This routine actually doesn't do much.

    """
    print("something: %r" % x)
    return fortran_stuff.foo()

