def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('skvideo', parent_package, top_path)

    # An example Fortran extension
    config.add_extension(
            'fortran_stuff',
            sources=['fortran_stuff.f90']
            )

    config.add_subpackage('tests')

    return config
