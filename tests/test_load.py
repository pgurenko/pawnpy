import os
import pawnpy
import subprocess

import unittest
from unittest.mock import MagicMock

basedir = os.path.dirname(os.path.realpath(__file__))


class TestLoad(unittest.TestCase):

    def test_load(self):
        pawnpy.cc(os.path.join(basedir, '../pawnpy/src/pawn/examples/hello2.p'),
                  basedir + '/hello2.amx',
                  os.path.join(basedir, '../pawnpy/src/pawn/include'))

        mock_sink = MagicMock()
        amx = pawnpy.AMX(basedir + '/hello2.amx', mock_sink)

    def test_load2(self):
        pawnpy.cc(basedir + '/test.p', output=basedir + '/test.amx')

        mock_sink = MagicMock()
        amx = pawnpy.AMX(basedir + '/test.amx', mock_sink)

        self.assertEqual(1, amx._exec(-1))  # main()
        mock_sink.bar.assert_called_with(1, 2, 3)
        mock_sink.buzz.assert_called_with(4, 5, 6, 7)

        self.assertEqual(2, amx._exec(0, 10, 8))  # foo()
        self.assertEqual(-2, amx._exec(0, 8, 10))
        self.assertEqual(1, amx.main())
        self.assertEqual(2, amx.foo(10, 8))
        self.assertEqual(-2, amx.foo(8, 10))

    def test_error(self):
        with self.assertRaises(subprocess.CalledProcessError):
            pawnpy.cc(basedir + '/test_error.p',
                      output=basedir + '/test_error.amx')
