import os
import unittest
import pawnpy

basedir = os.path.dirname(os.path.realpath(__file__))


class TestCompile(unittest.TestCase):

    def test_compile(self):
        pawnpy.cc(os.path.join(basedir, '../pawnpy/pawn/examples/hello.p'),
                  basedir + '/hello.amx',
                  os.path.join(basedir, '../pawnpy/pawn/include'))
