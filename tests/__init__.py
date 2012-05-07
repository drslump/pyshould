import unittest

from dsl import DslTestCase
from coordination import CoordinationTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DslTestCase))
    suite.addTest(unittest.makeSuite(CoordinationTestCase))
    return suite
