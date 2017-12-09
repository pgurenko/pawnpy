import os
import sys
from ctypes import (CDLL, POINTER, c_int, c_long,
                    create_string_buffer, c_char_p, c_void_p, byref,
                    memset, sizeof, CFUNCTYPE, Structure)
c_cell = c_int

basedir = os.path.dirname(os.path.realpath(__file__))

lib = CDLL(os.path.join(basedir, 'libpawnpy.so'))
lib.pc_compile.argtypes = (c_int, POINTER(c_char_p))


def cc(input, output=None, includes=None):
    argv = []
    argv.append('pawnc')
    argv.append(input)
    argv.append('-v2')
    if output:
        argv.append('-o' + output)
    if includes:
        argv.append('-i' + includes)

    arr = (c_char_p * len(argv))()
    for i, arg in enumerate(argv):
        arr[i] = arg.encode('utf-8')
    lib.pc_compile(len(argv), arr)


# /* reserve the first 15 error codes for exit codes of the abstract machine */
AMX_ERR_NONE = 0
AMX_ERR_EXIT = 1  # /* forced exit */
AMX_ERR_ASSERT = 2  # /* assertion failed */
AMX_ERR_STACKERR = 3  # /* stack/heap collision */
AMX_ERR_BOUNDS = 4  # /* index out of bounds */
AMX_ERR_MEMACCESS = 5  # /* invalid memory access */
AMX_ERR_INVINSTR = 6  # /* invalid instruction */
AMX_ERR_STACKLOW = 7  # * stack underflow */
AMX_ERR_HEAPLOW = 8  # /* heap underflow */
AMX_ERR_CALLBACK = 9  # /* no callback, or invalid callback */
AMX_ERR_NATIVE = 10  # /* native function failed */
AMX_ERR_DIVIDE = 11  # /* divide by zero */
AMX_ERR_SLEEP = 12  # /* go into sleepmode - code can be restarted */
AMX_ERR_INVSTATE = 13  # /* no implementation for this state, no fall-back */

AMX_ERR_MEMORY = 16,  # /* out of memory */
AMX_ERR_FORMAT = 17  # /* invalid file format */
AMX_ERR_VERSION = 18  # /* file is for a newer version of the AMX */
AMX_ERR_NOTFOUND = 19  # /* function not found */
AMX_ERR_INDEX = 20  # /* invalid index parameter (bad entry point) */
AMX_ERR_DEBUG = 21  # /* debugger cannot run */
AMX_ERR_INIT = 22  # /* AMX not initialized (or doubly initialized) */
AMX_ERR_USERDATA = 23  # /* unable to set user data field (table full) */
AMX_ERR_INIT_JIT = 24  # /* cannot initialize the JIT */
AMX_ERR_PARAMS = 25  # /* parameter error */
AMX_ERR_DOMAIN = 26  # /* domain error, expression result does not fit in range */
AMX_ERR_GENERAL = 27  # /* general error (unknown or unspecific error) */
AMX_ERR_OVERLAY = 28  # /* overlays are unsupported (JIT) or uninitialized */

sNAMEMAX = 31  # /* maximum name length of symbol name */


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

lib.amx_Init.argtypes = (POINTER(AMXNative), c_void_p)
lib.amx_Cleanup.argtypes = (POINTER(AMXNative),)
lib.amx_GetNative.argtypes = (POINTER(AMXNative), c_int, c_char_p)
lib.amx_GetPublic.argtypes = (
    POINTER(AMXNative), c_int, c_char_p, POINTER(c_int))
lib.amx_NumNatives.argtypes = (POINTER(AMXNative), POINTER(c_int))
lib.amx_NumPublics.argtypes = (POINTER(AMXNative), POINTER(c_int))
lib.amx_NumPubVars.argtypes = (POINTER(AMXNative), POINTER(c_int))
lib.amx_NumTags.argtypes = (POINTER(AMXNative), POINTER(c_int))
lib.amx_Push.argtypes = (POINTER(AMXNative), c_cell)
lib.amx_Exec.argtypes = (POINTER(AMXNative), POINTER(c_cell), c_int)
lib.amx_FindPublic.argtypes = (POINTER(AMXNative), c_char_p, POINTER(c_int))

class AMX():

    _binary_cache = {}

    def __init__(self, filename):
        self._filename = filename
        self._amx = AMXNative()
        memset(byref(self._amx), 0, sizeof(AMXNative))

        self._binary = AMX._binary_cache.get(filename, None)
        if not self._binary:
            with open(filename, mode='rb') as f:
                self._binary = f.read()
                AMX._binary_cache[filename] = self._binary

        result = lib.amx_Init(byref(self._amx), self._binary)
        if result != AMX_ERR_NONE:
            raise Exception('amx_Init failed with code %d' % result)

        numNatives = c_int()
        result = lib.amx_NumNatives(byref(self._amx), byref(numNatives))
        if result != AMX_ERR_NONE:
            raise Exception('amx_NumNatives failed with code %d' % result)

        print(numNatives)

        if numNatives.value != 0:
            name = create_string_buffer(sNAMEMAX + 1)
            result = lib.amx_GetNative(byref(self._amx), 0, name, None)
            if result != AMX_ERR_NONE:
                raise Exception('amx_GetNative failed with code %d' % result)

            print(name.value)

    def __del__(self):
        if self._amx.base:
            lib.amx_Cleanup(byref(self._amx))

        self._binary = None

        binary = AMX._binary_cache.get(self._filename, None)
        if binary:
            refs = sys.getrefcount(binary)
            if refs == 2:
                print('Cleaning up binary for %s' % self._filename)
                AMX._binary_cache.pop(self._filename)

    def exec(self, func_name, *args):
        """
        All you can eat function

        @param func_name: Name of public function to execute
        @param args: arguments to this function

        @return: whatever public function returns
        @throw: different execptions based  on different things
        """

        index = c_int()
        if func_name == 'main':
            index.value = -1
        else:
            if AMX_ERR_NONE != lib.amx_FindPublic(byref(self._amx), c_char_p(func_name.encode('utf-8')), byref(index)):
                raise KeyError("Public function %s not found" % func_name)

        for arg in reversed(args):
            #push them into stack
            lib.amx_Push(self._amx, arg)

        ret_val = c_int()
        err_code = lib.amx_Exec(byref(self._amx), byref(ret_val), index)
        if AMX_ERR_NONE != err_code:
            raise RuntimeError("Error calling %s function, code %d" % (func_name, err_code))

        return ret_val.value