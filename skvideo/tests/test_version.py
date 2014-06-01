# Example test file.

from numpy.testing import assert_equal
import skvideo

def test_version_good():
    assert_equal(skvideo.__version__, "0.1")
