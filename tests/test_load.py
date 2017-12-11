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
        # amx.exec('main')
        # amx.main()

    def test_load2(self):
        pawnpy.cc(basedir + '/test.p', output=basedir + '/test.amx')
        amx = pawnpy.AMX(basedir + '/test.amx')
        self.assertEqual(1, amx._exec('main'))
        self.assertEqual(2, amx._exec('foo', 10, 8))
        self.assertEqual(-2, amx._exec('foo', 8, 10))
