import unittest
import pawnpy

class TestCompile(unittest.TestCase):
    def test_compile(self):
        pawnpy.cc('../pawnpy/src/pawn/examples/hello.p')
