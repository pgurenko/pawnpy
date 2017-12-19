# PawnPy

[![Build Status](https://travis-ci.org/pgurenko/pawnpy.svg?branch=master)](https://travis-ci.org/pgurenko/pawnpy)

Python wrapper for [pawn](https://github.com/compuphase/pawn) virtual machine.

Compile, run and debug pawn scripts within easily-to-use environment.

For example:

```python
import pawnpy

pawnpy.cc('./hello.p', './hello.amx')
amx = pawnpy.AMX('./hello.amx')
amx.main()
```

The wrapper itself is the ctypes-based Python library plus pawn library built for major platforms.
