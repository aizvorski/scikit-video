from skvideo.version import __version__

# If you want to use Numpy's testing framerwork, use the following.
# Tests go under directory tests/, benchmarks under directory benchmarks/
from numpy.testing import Tester
test = Tester().test
bench = Tester().bench
