"Actual (primitive) types instanitated in the type system."

import sys

from .typesys import *


class np:
    # Dummy
    class ndarray:
        pass


int32 = TCon("Int32")
int64 = TCon("Int64")
float32 = TCon("Float")
double64 = TCon("Double")
void = TCon("Void")
