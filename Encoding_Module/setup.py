# from distutils.core import setup
# from Cython.Build import cythonize
#
# setup(ext_modules=cythonize('speedUp.pyx'))


from distutils.core import setup, Extension

module = Extension('book', sources = ['aux.c', 'struct.h'])

setup(name = 'book',
      version = '1.0',
      description = 'This is a demo package',
      ext_modules = [module])
