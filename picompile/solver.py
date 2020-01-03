"Constraint Solver, Robinson algorithm"

from collections import deque

from .typesys import *


def empty():
    return {}


def apply(s, t):
    if isinstance(t, TCon):
        return t
    elif isinstance(t, TApp):
        return TApp(apply(s, t.a), apply(s, t.b))
    elif isinstance(t, TFun):
        argtys = [apply(s, a) for a in t.argtys]
        retty = apply(s, t.retty)
        return TFun(argtys, retty)
    elif isinstance(t, TVar):
        return s.get(t.s, t)


def applyList(s, xs):
    return [(apply(s, x), apply(s, y)) for (x, y) in xs]


def unify(x, y):
    if isinstance(x, TApp) and isinstance(y, TApp):
        s1 = unify(x.a, y.a)
        s2 = unify(apply(s1, x.b), apply(s1, y.b))
        return compose(s2, s1)
    elif isinstance(x, TCon) and isinstance(y, TCon) and (x == y):
        return empty()
    elif isinstance(x, TFun) and isinstance(y, TFun):
        if len(x.argtys) != len(y.argtys):
            return Exception("Wrong number of arguments")
        s1 = solve(zip(x.argtys, y.argtys))
        s2 = unify(apply(s1, x.retty), apply(s1, y.retty))
        return compose(s2, s1)
    elif isinstance(x, TVar):
        return bind(x.s, y)
    elif isinstance(y, TVar):
        return bind(y.s, x)
    else:
        raise InferError(x, y)


def solve(xs):
    mgu = empty()
    cs = deque(xs)
    while len(cs):
        (a, b) = cs.pop()
        s = unify(a, b)
        mgu = compose(s, mgu)
        cs = deque(applyList(s, cs))
    return mgu


def bind(n, x):
    if x == n:
        return empty()
    elif occurs_check(n, x):
        raise InfiniteType(n, x)
    else:
        return dict([(n, x)])


def occurs_check(n, x):
    return n in ftv(x)


def union(s1, s2):
    nenv = s1.copy()
    nenv.update(s2)
    return nenv


def compose(s1, s2):
    s3 = dict((t, apply(s1, u)) for t, u in s2.items())
    return union(s1, s3)
