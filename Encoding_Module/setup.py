from distutils.core import setup
from Cython.Build import cythonize
import numpy

# setup(ext_modules=cythonize('speedUp.pyx'))

setup(ext_modules=cythonize('fast.pyx'), include_dirs=[numpy.get_include()])

# from distutils.core import setup, Extension
#
# module = Extension('exmod', include_dirs=['/usr/local/include'], libraries=['pthread'], sources=['exmodmodule.c'])
# setup(name='exmod', version='1.0', description='This is my package', ext_modules=[module])
