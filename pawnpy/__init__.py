import os
import sys
import subprocess
from ctypes import (CDLL, POINTER, c_int, c_long,
                    create_string_buffer, c_char_p, c_void_p, byref,
                    memset, sizeof, CFUNCTYPE, Structure)
c_cell = c_int

basedir = os.path.dirname(os.path.realpath(__file__))

if sys.maxsize > 2**32:
    bitness = '.x64'
else:
    bitness = '.x86'

ccname = 'pawncc'

if sys.platform == 'win32':
    ccname +=  bitness + '.exe'
else:
    if not os.path.exists(os.path.join(basedir, ccname)):
        if sys.platform == 'darwin':
            ccname += '.darwin' + bitness
        else:
            ccname += '.linux' + bitness

def cc(input, output=None, includes=None):
    argv = []
    argv.append(os.path.join(basedir, ccname))
    argv.append(input)
    argv.append('-v2')
    if output:
        argv.append('-o' + output)
    if includes:
        argv.append('-i' + includes)

    arr = (c_char_p * len(argv))()
    for i, arg in enumerate(argv):
        arr[i] = arg.encode('utf-8')
    subprocess.check_call(argv)

libname = 'pawnpy'

if sys.platform == 'win32':
    libname +=  bitness + '.dll'
else:
    libname = 'lib' + libname
    if sys.platform == 'darwin':
        if os.path.exists(os.path.join(basedir, libname + '.dylib')):
            libname += '.dylib'
        else:
            libname += '.darwin' + bitness + '.dylib'
    else:
        if os.path.exists(os.path.join(basedir, libname + '.so')):
            libname += '.so'
        else:
            libname += '.linux' + bitness + '.so'

lib = CDLL(os.path.join(basedir, libname))

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


class AMX_NATIVE_INFO(Structure):

    _pack_ = 1

    _fields_ = [
        ('name', c_char_p),
        ('func', AMX_NATIVE),
    ]


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
lib.amx_Register.argtypes = (
    POINTER(AMXNative), POINTER(AMX_NATIVE_INFO), c_int)
lib.amx_SetCallback.argtypes = (POINTER(AMXNative), AMX_CALLBACK)

# aux functions to simplify loading
lib.aux_LoadProgram.argtypes = (POINTER(AMXNative), c_char_p, c_void_p)
lib.aux_FreeProgram.argtypes = (POINTER(AMXNative),)


class AMX():

    def __init__(self, filename, native_sink):
        self._filename = filename
        self._native_sink = native_sink
        self._amx = AMXNative()

        result = lib.aux_LoadProgram(
            byref(self._amx), c_char_p(filename.encode('utf-8')), 0)
        if result != AMX_ERR_NONE:
            raise RuntimeError('aux_LoadProgram failed with code %d' % result)

        self._publics = None
        self.__init_publics()

        self._natives = None
        self.__init_natives()

    def __init_publics(self):
        """Fills publics info and hooks them up to AMX attrs"""

        setattr(self, 'main', lambda *args: self._exec(-1, *args))

        num_publics = c_int()
        err_code = lib.amx_NumPublics(byref(self._amx), byref(num_publics))
        if AMX_ERR_NONE != err_code:
            raise RuntimeError('amx_NumPublics failed with code %d' % err_code)

        self._publics = []

        for i in range(num_publics.value):
            name = create_string_buffer(sNAMEMAX + 1)

            err_code = lib.amx_GetPublic(byref(self._amx), i, name, None)
            if AMX_ERR_NONE != err_code:
                raise RuntimeError(
                    'amx_GetPublic failed with code %d' % err_code)

            name = str(name.value, 'utf-8')
            self._publics.append(name)

            setattr(self, name, lambda *args,
                    func_id=i: self._exec(func_id, *args))

    def __init_natives(self):
        num_natives = c_int()
        err_code = lib.amx_NumNatives(byref(self._amx), byref(num_natives))
        if err_code != AMX_ERR_NONE:
            raise RuntimeError('amx_NumNatives failed with code %d' % err_code)

        if num_natives.value == 0:
            return

        self._natives = (AMX_NATIVE_INFO * num_natives.value)()
        self._callbacks = []

        for i in range(num_natives.value):
            name = create_string_buffer(sNAMEMAX + 1)
            err_code = lib.amx_GetNative(byref(self._amx), i, name, None)
            if err_code != AMX_ERR_NONE:
                raise RuntimeError(
                    'amx_GetNative failed with code %d' % err_code)

            self._callbacks.append(
                getattr(self._native_sink, str(name.value, 'utf-8')))

            self._natives[i].name = name.value
            self._natives[i].func = AMX_NATIVE(lambda amx, params: 0)

        lib.amx_Register(self._amx, self._natives, num_natives.value)

        def callback(amx, index, result, params):
            argc = int(params[0] / sizeof(c_cell))
            argv = [params[i] for i in range(1, argc + 1)]
            result.value = self._callbacks[index](*argv)
            return 0

        self._callback = AMX_CALLBACK(callback)

        lib.amx_SetCallback(self._amx, self._callback)

    def __del__(self):
        if self._amx.base:
            lib.aux_FreeProgram(byref(self._amx))

    def _exec(self, func_id, *args):
        """
        All you can eat function

        @param func_id: Id of public function to execute
        @param args: arguments to this function

        @return: whatever public function returns
        @throw: different execptions based  on different things
        """

        for arg in reversed(args):
            # push them into stack
            lib.amx_Push(self._amx, arg)

        index = c_int(func_id)
        ret_val = c_int()
        err_code = lib.amx_Exec(byref(self._amx), byref(ret_val), index)
        if AMX_ERR_NONE != err_code:
            func_name = 'main' if func_id == -1 else self._publics[func_id]
            raise RuntimeError(
                "amx_Exec failed for %s, code %d" % (func_name, err_code))

        return ret_val.value
