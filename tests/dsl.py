import unittest
from pyshould import *
from pyshould import dsl
from pyshould import Expectation

class DslTestCase(unittest.TestCase):
    """ Simple tests for the exposed DSL symbols """

    def test_keywords(self):
        keywords = (
            'should', 'should_not', 'should_any', 'should_all', 
            'should_none', 'should_either', 
            'it', 'all_of', 'any_of', 'none_of'
        )

        for kw in keywords:
            self.assertTrue(kw in globals(), msg='keyword "%s" not found as global' % kw)
            self.assertTrue(kw in dir(dsl), msg='keyword "%s" not found in dsl' % kw)

    def test_expectations(self):
        self.assertIsInstance(should, Expectation)
        self.assertIsInstance(should_not, Expectation)
        self.assertIsInstance(should_any, Expectation)
        self.assertIsInstance(should_all, Expectation)
        self.assertIsInstance(should_none, Expectation)
        self.assertIsInstance(should_either, Expectation)

    def test_quantifiers(self):
        self.assertIsInstance(it(0), Expectation)
        self.assertIsInstance(all_of([]), Expectation)
        self.assertIsInstance(any_of([]), Expectation)
        self.assertIsInstance(none_of([]), Expectation)


    def test_should(self):
        self.assertRaises(AssertionError, lambda: 0 | should.equal(1))

    def test_should_not(self):
        self.assertRaises(AssertionError, lambda: 0 | should_not.equal(0))

    def test_should_either(self):
        0 | should_either.equal(1).equal(0)

    def test_should_all(self):
        self.assertRaises(AssertionError, lambda: [0,1] | should.equal(0))

    def test_should_any(self):
        self.assertRaises(AssertionError, lambda: [0,1] | should.equal(2))

    def test_should_none(self):
        self.assertRaises(AssertionError, lambda: [0,1] | should.equal(1))


    def test_it(self):
        self.assertRaises(AssertionError, lambda: it(0).equal(1))

    def test_all_of(self):
        self.assertRaises(AssertionError, lambda: all_of([1,2]).equal(1))
        self.assertRaises(AssertionError, lambda: all_of((1,2)).equal(1))
        self.assertRaises(AssertionError, lambda: all_of(1,2).equal(1))

    def test_any_of(self):
        self.assertRaises(AssertionError, lambda: any_of([2,2]).equal(1))
        self.assertRaises(AssertionError, lambda: any_of((2,2)).equal(1))
        self.assertRaises(AssertionError, lambda: any_of(2,2).equal(1))

    def test_none_of(self):
        self.assertRaises(AssertionError, lambda: none_of([2,1]).equal(1))
        self.assertRaises(AssertionError, lambda: none_of((2,1)).equal(1))
        self.assertRaises(AssertionError, lambda: none_of(2,1).equal(1))

