import sys
from distutils.core import setup

libname = 'pawnpy'

if sys.maxsize > 2**32:
    bitness = '.x64'
else:
    bitness = '.x86'

if sys.platform == 'win32':
    libname +=  bitness + '.dll'
else:
    libname = 'lib' + libname
    if sys.platform == 'darwin':
        libname += '.darwin' + bitness + '.dylib'
    else:
        libname += '.linux' + bitness + '.so'

setup(
    name='pawnpy',
    version='1.0',
    description='Pawn wrapper for Python',
    author='Pavel Gurenko & Dmitry Efremov',
    author_email='pgurenko@gmail.com',
    url='https://github.com/pgurenko/pawnpy',
    download_url='https://github.com/pgurenko/pawnpy/archive/1.0.tar.gz',
    keywords=['pawn', 'wrapper', 'testing'],
    classifiers=[],
    packages=['pawnpy'],
    package_data={'pawnpy': [libname]}
)
