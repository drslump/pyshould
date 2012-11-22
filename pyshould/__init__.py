"""
pyshould - a should style wrapper for pyhamcrest
"""
from pyshould.dsl import *

__author__  = "Ivan -DrSlump- Montes"
__email__   = "drslump@pollinimini.net"
__license__ = "MIT"

# Override the list public symbols for a wildcard import
__all__ = [
    'should',
    'should_not',
    'should_any',
    'should_all',
    'should_none',
    'should_either',
    'it',
    'all_of',
    'any_of',
    'none_of',
]


# Patch mockito param matcher to use pyshould expectations
try:
    import mockito
    from pyshould.expectation import Expectation

    original_method = mockito.invocation.MatchingInvocation.compare

    @staticmethod
    def pyshould_compare(p1, p2):
        if isinstance(p1, Expectation):
            try:
                expectation = p1.clone()
                expectation.resolve(p2)
                return True
            except AssertionError:
                return False
        return original_method(p1, p2)

except ImportError:
    pass
