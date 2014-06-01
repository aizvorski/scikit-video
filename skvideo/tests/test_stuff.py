from numpy.testing import assert_allclose

from skvideo import stuff

def test_do_something():
    assert_allclose(stuff.do_something(9), [4, 3, 2, 1])
