import sys
import ast

from picompile.py2coreast import PythonVisitor
from picompile.infer import typeinfer
from picompile import rtman


source = open(sys.argv[1]).read()
tree = ast.parse(source)
print(ast.dump(tree))

py2interim = PythonVisitor()

interim_tree = py2interim.visit(tree)
print(ast.dump(interim_tree))

ty, mgu = typeinfer(interim_tree)
print("ty:", ty)
print("mgu:", mgu)

#fun = rtman.specialize_and_call(interim_tree, ty, mgu, (10, 25))
fun = rtman.jit_specialize(interim_tree, ty, mgu)
print(fun)
print(fun(10, 15))
