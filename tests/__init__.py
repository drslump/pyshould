import unittest

from dsl import DslTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DslTestCase))
    return suite
