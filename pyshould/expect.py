import pyshould

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"


def expect(value, *args):
    if len(args):
        return expect_all(value, *args)
    else:
        return expect_it(value)


def expect_it(value):
    return pyshould.it(value)


def expect_all(*args):
    return pyshould.all_of(*args)


def expect_any(*args):
    return pyshould.any_of(*args)


def expect_none(*args):
    return pyshould.none_of(*args)
