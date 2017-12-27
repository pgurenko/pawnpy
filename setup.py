import sys
from distutils.core import setup

version = '1.0.1'

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

ccname = 'pawncc'

if sys.platform == 'win32':
    ccname +=  bitness + '.exe'
else:
    if sys.platform == 'darwin':
        ccname += '.darwin' + bitness
    else:
        ccname += '.linux' + bitness

setup(
    name='pawnpy',
    version=version,
    description='Pawn wrapper for Python',
    author='Pavel Gurenko & Dmitry Efremov',
    author_email='pgurenko@gmail.com',
    url='https://github.com/pgurenko/pawnpy',
    download_url='https://github.com/pgurenko/pawnpy/releases/download/%s/pawnpy-%s.tar.gz' % (version, version),
    keywords=['pawn', 'wrapper', 'testing'],
    classifiers=[],
    packages=['pawnpy'],
    package_data={'pawnpy': [libname, ccname]}
)
