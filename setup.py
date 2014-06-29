#!/usr/bin/env python
descr = """\
Video Processing SciKit

Video processing algorithms for SciPy, including IO, quality metrics, filtering, etc.

"""

DISTNAME            = 'scikit-video'
DESCRIPTION         = 'Video processing routines for SciPy'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Alex Izvorski',
MAINTAINER_EMAIL    = 'aizvorski@gmail.com',
URL                 = 'https://github.com/aizvorski/scikit-video/'
LICENSE             = 'GPLv3'
DOWNLOAD_URL        = URL
PACKAGE_NAME        = 'skvideo'
EXTRA_INFO          = dict(
    install_requires=['numpy'],
    classifiers=['Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: C',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Topic :: Multimedia :: Video',
            'Topic :: Multimedia :: Video :: Conversion',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            ]
)


import os
import sys
import subprocess

import setuptools
from numpy.distutils.core import setup

def configuration(parent_package='', top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg: "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage(PACKAGE_NAME)
    return config

def get_version():
    """Obtain the version number"""
    import imp
    mod = imp.load_source('version', os.path.join(PACKAGE_NAME, 'version.py'))
    return mod.__version__

# Documentation building command
try:
    from sphinx.setup_command import BuildDoc as SphinxBuildDoc
    class BuildDoc(SphinxBuildDoc):
        """Run in-place build before Sphinx doc build"""
        def run(self):
            ret = subprocess.call([sys.executable, sys.argv[0], 'build_ext', '-i'])
            if ret != 0:
                raise RuntimeError("Building Scipy failed!")
            SphinxBuildDoc.run(self)
    cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
    cmdclass = {}

# Call the setup function
if __name__ == "__main__":
    setup(configuration=configuration,
          name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          include_package_data=True,
          test_suite="nose.collector",
          cmdclass=cmdclass,
          version=get_version(),
          **EXTRA_INFO)
