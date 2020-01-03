from .typesys import *
from .solver import solve, apply, unify, compose


def naming():
    k = 0
    while True:
        yield "t%d" % k
        k += 1


class TypeInfer(object):

    def __init__(self):
        self.constraints = []
        self.env = {}
        self.names = naming()

    def fresh(self):
        return TVar('$' + next(self.names))  # New meta type variable.

    def visit(self, node):
        name = "visit_%s" % type(node).__name__
        if hasattr(self, name):
            return getattr(self, name)(node)
        else:
            return self.generic_visit(node)

    def visit_Fun(self, node):
        self.argtys = [self.fresh() for v in node.args]
        self.retty = TVar("$retty")
        for arg, ty in zip(node.args, self.argtys):
            arg.type = ty
            self.env[arg.id] = ty
        list(map(self.visit, node.body))
        return TFun(self.argtys, self.retty)

    def visit_Noop(self, node):
        return None

    def visit_LitInt(self, node):
        tv = self.fresh()
        node.type = tv
        return tv

    def visit_LitFloat(self, node):
        tv = self.fresh()
        node.type = tv
        return tv

    def visit_Assign(self, node):
        ty = self.visit(node.val)
        if node.ref in self.env:
            # Subsequent uses of a variable must have the same type.
            self.constraints += [(ty, self.env[node.ref])]
        self.env[node.ref] = ty
        node.type = ty
        return None

    def visit_Index(self, node):
        tv = self.fresh()
        ty = self.visit(node.val)
        ixty = self.visit(node.ix)
        self.constraints += [(ty, array(tv)), (ixty, int32)]
        return tv

    def visit_Prim(self, node):
        if node.fn == "shape#":
            return array(int32)
        elif node.fn == "mult#":
            tya = self.visit(node.args[0])
            tyb = self.visit(node.args[1])
            self.constraints += [(tya, tyb)]
            return tyb
        elif node.fn == "add#":
            tya = self.visit(node.args[0])
            tyb = self.visit(node.args[1])
            self.constraints += [(tya, tyb)]
            return tyb
        else:
            raise NotImplementedError

    def visit_Var(self, node):
        ty = self.env[node.id]
        node.type = ty
        return ty

    def visit_Return(self, node):
        ty = self.visit(node.val)
        self.constraints += [(ty, self.retty)]

    def visit_Loop(self, node):
        self.env[node.var.id] = int32
        varty = self.visit(node.var)
        begin = self.visit(node.begin)
        end = self.visit(node.end)
        self.constraints += [(varty, int32), (
            begin, int64), (end, int32)]
        list(map(self.visit, node.body))

    def generic_visit(self, node):
        raise NotImplementedError


def typeinfer(ast):
    infer = TypeInfer()
    ty = infer.visit(ast)
    print("fun type:", ty)
    print("constraints:", infer.constraints)
    # Most general unifier
    mgu = solve(infer.constraints)
    #print("mgu:", mgu)
    infer_ty = apply(mgu, ty)
    #print("infer_ty:", infer_ty)
    return infer_ty, mgu


def spec_types(infer_ty, mgu, argtys):
    spec_ty = TFun(argtys=argtys, retty=TVar("$retty"))
    unifier = unify(infer_ty, spec_ty)
    specializer = compose(unifier, mgu)
    print("Specialized types:", specializer)

    retty = apply(specializer, TVar("$retty"))
    argtys = [apply(specializer, ty) for ty in argtys]
    print("Specialized Function:", TFun(argtys, retty))

    if determined(retty) and all(map(determined, argtys)):
        return specializer, retty, argtys
    else:
        raise UnderDetermined()
