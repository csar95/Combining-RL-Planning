# from distutils.core import setup
# from Cython.Build import cythonize
#
# setup(ext_modules=cythonize('speedUp.pyx'))

from distutils.core import setup, Extension

module = Extension('exmod', include_dirs=['/usr/local/include'], libraries=['pthread'], sources=['exmodmodule.c'])
setup(name='exmod', version='1.0', description='This is my package', ext_modules=[module])
