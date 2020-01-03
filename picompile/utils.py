def mangler(fname, sig):
    "Mangle function name based on argument types."
    return fname + str(hash(tuple(sig)))
