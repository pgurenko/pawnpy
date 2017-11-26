# PawnPy

Python wrapper for [pawn](https://github.com/compuphase/pawn) virtual machine.

The goal is to build, run and debug pawn scripts within easily-to-use environment.

For example:

```python
import pawn

pawn.compile('hello.p', 'hello.amx')
pawn.AMX amx = pawn.load('hello.amx')
amx.some_func()
```

The wrapper itself is the C++ extension for Python using boost python to interface Python and pawn library to interface pawn.
