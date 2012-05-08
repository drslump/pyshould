import unittest

from dsl import DslTestCase
from coordination import CoordinationTestCase
from expect import ExpectTestCase

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DslTestCase))
    suite.addTest(unittest.makeSuite(CoordinationTestCase))
    suite.addTest(unittest.makeSuite(ExpectTestCase))
    return suite

