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
