import ctypes

from .types import *

__all__ = ("wrap_function",)


def _type_numpile2ctypes(typ):
    print(typ)
    if typ == int64:
        ctype = ctypes.c_int64
    else:
        assert 0
    return ctype


def wrap_function(func_name, func_addr, retty, argtys):
    ret_ctype = _type_numpile2ctypes(retty)
    args_ctypes = [_type_numpile2ctypes(a) for a in argtys]
    functype = ctypes.CFUNCTYPE(ret_ctype, *args_ctypes)

    cfunc = functype(func_addr)
    cfunc.__name__ = func_name

    dispatch = arg_lowerer(cfunc)
    return dispatch


def lower_arg(arg, val):
    if isinstance(val, np.ndarray):
        ndarray = arg._type_
        data, dims, shape = wrap_ndarray(val)
        return ndarray(data, dims, shape)
    else:
        return val


def arg_lowerer(fn):
    "Wrapper which lowers passed in args on the fly."

    def _lower_and_call(*args):
        rargs = list(map(lower_arg, fn._argtypes_, args))
        return fn(*rargs)

    #_lower_and_call.__name__ = fn.__name__
    return _lower_and_call
