picompile
=========

Pico Compile (picompile) is a project to further develop `numpile` sample
by Stephen Diehl, which is a minimalist, LLVM-based JIT compiler for
statically-typable Python subset. Picompile primarily targets
[Pycopy](https://github.com/pfalcon/pycopy), a minimalist Python
implementation, but also should be compatible with CPython and other
Python implementations.

Picompile starts with factoring out monolithic `numpile` codebase into a
set of simple and small modules, to make dependency patterns among them
clearer.

Just as the original `numpile` project, `picompile` is intended to be
suitable for studying, and thus minimalism and clarity of changes is
important. Due to this, the repository is rebased, to avoid useless
noise in the change history.

Credits and licensing
---------------------

Picompile is based on [numpile](https://github.com/sdiehl/numpile)
project, Copyright (c) 2015-2017, Stephen Diehl.

Picompile is Copyright (c) 2019-2020,
[Paul Sokolovsky](https://github.com/pfalcon) and is released under
the MIT license.
