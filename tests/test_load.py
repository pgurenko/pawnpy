import os
import unittest
import pawnpy

basedir = os.path.dirname(os.path.realpath(__file__))


class TestLoad(unittest.TestCase):

    def test_load(self):
        pawnpy.cc(os.path.join(basedir, '../pawnpy/src/pawn/examples/hello2.p'),
                  basedir + '/hello2.amx',
                  os.path.join(basedir, '../pawnpy/src/pawn/include'))
        amx = pawnpy.AMX(basedir + '/hello2.amx')
        # amx.main()
