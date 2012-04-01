import pyshould

def expect(*args):
    if len(args) > 1:
        return expect_all(args)
    else:
        return expect_it(args[0])

def expect_it(value):
    return pyshould.it(value)

def expect_all(value):
    return pyshould.all_of(value)

def expect_any(value):
    return pyshould.any_of(value)

def expect_none(value):
    return pyshould.none_of(value)

