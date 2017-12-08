import os
from ctypes import (CDLL, POINTER, c_int, c_long,
                    c_char_p, c_void_p, addressof,
                    memset, sizeof, CFUNCTYPE, Structure)

c_cell = c_int

basedir = os.path.dirname(os.path.realpath(__file__))

lib = CDLL(os.path.join(basedir, 'libpawnpy.so'))
lib.pc_compile.argtypes = (c_int, POINTER(c_char_p))


def cc(input, output=None, includes=None):
    argv = []
    argv.append('pawnc')
    argv.append(input)
    if output:
        argv.append('-o' + output)
    if includes:
        argv.append('-i' + includes)

    arr = (c_char_p * len(argv))()
    for i, arg in enumerate(argv):
        arr[i] = arg.encode('utf-8')
    lib.pc_compile(len(argv), arr)


class AMXNative(Structure):
    pass

# typedef c_cell (AMX_NATIVE_CALL *AMX_NATIVE)(struct tagAMX *amx, const
# cell *params);
AMX_NATIVE = CFUNCTYPE(c_cell, POINTER(AMXNative), POINTER(c_cell))
# typedef int (AMXAPI *AMX_CALLBACK)(struct tagAMX *amx, cell index,
# cell *result, const c_cell *params);
AMX_CALLBACK = CFUNCTYPE(
    c_int, POINTER(AMXNative), c_cell, POINTER(c_cell), POINTER(c_cell))
# typedef int (AMXAPI *AMX_DEBUG)(struct tagAMX *amx);
AMX_DEBUG = CFUNCTYPE(c_int, POINTER(AMXNative))
# typedef int (AMXAPI *AMX_OVERLAY)(struct tagAMX *amx, int index);
AMX_OVERLAY = CFUNCTYPE(c_int, POINTER(AMXNative), c_int)
# typedef int (AMXAPI *AMX_IDLE)(struct tagAMX *amx, int AMXAPI
# Exec(struct tagAMX *, c_cell *, int));
AMX_EXEC = CFUNCTYPE(c_int, POINTER(AMXNative), POINTER(c_cell), c_int)
AMX_IDLE = CFUNCTYPE(c_int, POINTER(AMXNative), c_int, AMX_EXEC)

AMX_USERNUM = 4

AMXNative._fields_ = [
    # points to the AMX header, perhaps followed by P-code and data
    ('base', c_void_p),
    # points to P-code block, possibly in ROM or in an overlay pool
    ('code', c_void_p),
    # points to separate data+stack+heap, may be NULL
    ('data', c_void_p),
    # native function callback
    ('callback', AMX_CALLBACK),
    # debug callback
    ('debug', AMX_DEBUG),
    # overlay reader callback
    ('overlay', AMX_OVERLAY),
    # for external functions a few registers must be accessible from
    # the outside

    # instruction pointer: relative to base + amxhdr->cod
    ('cip', c_cell),
    # stack frame base: relative to base + amxhdr->dat
    ('frm', c_cell),
    # top of the heap: relative to base + amxhdr->dat
    ('hea', c_cell),
    #  bottom of the heap: relative to base + amxhdr->dat
    ('hlw', c_cell),
    # stack pointer: relative to base + amxhdr->dat
    ('stk', c_cell),
    # top of the stack: relative to base + amxhdr->dat
    ('stp', c_cell),
    # current status, see amx_Flags()
    ('flags', c_int),

    #   user data
    #   #if AMX_USERNUM > 0
    ('usertags', c_long * AMX_USERNUM),
    ('userdata', c_void_p * AMX_USERNUM),
    #   #endif

    # native functions can raise an error
    ('error', c_int),
    # passing parameters requires a 'count' field
    ('paramcount', c_int),
    # the sleep opcode needs to store the full AMX status
    ('pri', c_cell),
    ('alt', c_cell),
    ('reset_stk', c_cell),
    ('reset_hea', c_cell),
    # extra fields for increased performance
    # relocated address/value for the SYSREQ.D opcode
    ('sysreq_d', c_cell),
    # fields for overlay support and JIT support
    # current overlay index
    ('ovl_index', c_int),
    # size of the overlay, or estimated memory footprint of the native
    # code
    ('codesize', c_long),

    # #if defined AMX_JIT
    #   /* support variables for the JIT */
    #   int reloc_size; /* required temporary buffer for relocations */
    # #endif
]

AMXNative._pack_ = 1

lib.amx_Init.argtypes = (c_int, POINTER(AMXNative), c_void_p)


class AMX():

    def __init__(self, filename):
        self._amx = AMXNative()
        memset(addressof(self._amx), 0, sizeof(AMXNative))

        with open(fileName, mode='rb') as file:
            content = file.read()
            amx_Init(addressof(self._amx), content)
