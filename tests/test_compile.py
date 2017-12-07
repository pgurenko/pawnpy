import os
import unittest
import pawnpy

basedir = os.path.dirname(os.path.realpath(__file__))


class TestCompile(unittest.TestCase):

    def test_compile(self):
        pawnpy.cc('/home/pavel/pawnpy/pawnpy/src/pawn/examples/hello.p',
                  basedir + '/hello.amx',
                  '/home/pavel/pawnpy/pawnpy/src/pawn/include')
