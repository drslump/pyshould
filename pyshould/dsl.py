"""
Define the names making up the domain specific language
"""

from pyshould.expectation import (
        Expectation, ExpectationNot,
        ExpectationAll, ExpectationAny,
        ExpectationNone, OPERATOR
)

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"

# Create instances to be used with the overloaded | operator
should = Expectation(deferred=True)
should_not = ExpectationNot(deferred=True)
should_all = ExpectationAll(deferred=True)
should_any = ExpectationAny(deferred=True)
should_none = ExpectationNone(deferred=True)
should_either = Expectation(deferred=True, def_op=OPERATOR.OR)


def it(value):
    """ Wraps a value in an exepctation """
    return Expectation(value)


def any_of(value, *args):
    """ At least one of the items in value should match """

    if len(args):
        value = (value,) + args

    return ExpectationAny(value)


def all_of(value, *args):
    """ All the items in value should match """

    if len(args):
        value = (value,) + args

    return ExpectationAll(value)


def none_of(value, *args):
    """ None of the items in value should match """

    if len(args):
        value = (value,) + args

    return ExpectationNone(value)
