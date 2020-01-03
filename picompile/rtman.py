from .types import *
from .codegen import codegen
from .utils import mangler
from .call import wrap_function
from .infer import spec_types


function_cache = {}


def arg_pytype(arg):
    if isinstance(arg, int) and arg <= sys.maxsize:
        return int64
    elif isinstance(arg, float):
        return double64
    else:
        raise Exception("Type not supported: %s" % type(arg))


def specialize_and_call(ast, infer_ty, mgu, args):
    arg_types = list(map(arg_pytype, list(args)))
    specializer, retty, argtys = spec_types(infer_ty, mgu, arg_types)
    key = mangler(ast.fname, argtys)
    # Don't recompile after we've specialized.
    if key in function_cache:
        return function_cache[key](*args)
    else:
        print("Calling codegen with:", retty, argtys)
        cgen = codegen(ast, specializer, retty, argtys)
        pyfunc = wrap_function(cgen.function.name, cgen.get_func_addr(), retty, argtys)
        function_cache[key] = pyfunc
        return pyfunc(*args)


def jit_specialize(ast, infer_ty, mgu):
    "Specialize a function on an actual call."

    def _wrapper(*args):
        return specialize_and_call(ast, infer_ty, mgu, args)

    return _wrapper
