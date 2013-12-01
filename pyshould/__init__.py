"""
pyshould - a should style wrapper for pyhamcrest
"""
from pyshould.dsl import *

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"


def print_help():
    from pyshould.matchers import lookup, aliases, alias_help
    group = {}
    for alias in aliases():
        m = lookup(alias)
        if m not in group:
            group[m] = []
        group[m].append(alias)

    for items in group.values():
        print("{0}:\n\t{1}\n".format(
            ', '.join(items),
            alias_help(items[0]).replace("\n", "\n\t")
        ))


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
    'none_of'
]
