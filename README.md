# PawnPy

[![Build Status](https://travis-ci.org/pgurenko/pawnpy.svg?branch=master)](https://travis-ci.org/pgurenko/pawnpy)

Python wrapper for [pawn](https://github.com/compuphase/pawn) virtual machine.

The goal is to build, run and debug pawn scripts within easily-to-use environment.

For example:

```python
import pawnpy

src = pawnpy.Source(filename='./hello.p')
src.set_breakpoint(line=3)

amx = src.compile(output='./hello.amx')
amx.some_func()
```

The wrapper itself is the C++ extension for Python using boost python to interface Python and pawn library to interface pawn.
