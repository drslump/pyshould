import unittest
from pyshould import Expectation, OPERATOR

class CoordinationTestCase(unittest.TestCase):
    """ Test coordination of complex expectations """

    def test_implicit_and(self):
        ex = Expectation(deferred=True)

        ex.less_than(1).less_than(2)
        ex.resolve(0)

        ex.less_than(1).less_than(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(1))
        ex.less_than(2).less_than(1)
        self.assertRaises(AssertionError, lambda: ex.resolve(1))

    def test_explicit_and(self):
        ex = Expectation(deferred=True)

        ex.less_than(1).and_less_than(2)
        ex.resolve(0)

        ex.less_than(1).and_less_than(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(1))
        ex.less_than(2).And_less_than(1)
        self.assertRaises(AssertionError, lambda: ex.resolve(1))

    def test_implicit_or(self):
        ex = Expectation(deferred=True, def_op = OPERATOR.OR)

        ex.equal(1).equal(0)
        ex.resolve(0)

        ex.equal(0).equal(1)
        ex.resolve(0)

        ex.equal(1).equal(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(0))

    def test_explicit_or(self):
        ex = Expectation(deferred=True)

        ex.equal(1).or_equal(0)
        ex.resolve(0)

        ex.equal(0).Or_equal(1)
        ex.resolve(0)

        ex.equal(1).OR_equal(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(0))

    def test_precedence(self):
        ex = Expectation(deferred=True)

        ex.equal(3). or_equal(0).and_less_than(2)
        ex.resolve(0)

        ex.equal(3). or_equal(0).and_less_than(2)
        ex.resolve(3)

        ex.equal(3). or_equal(0).and_less_than(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(4))

        ex.equal(0).or_equal(10) .but_less_than(5)
        ex.resolve(0)

        ex.equal(0).or_equal(10) .but_less_than(5)
        self.assertRaises(AssertionError, lambda: ex.resolve(3))
        ex.equal(0).or_equal(10) .but_less_than(5)
        self.assertRaises(AssertionError, lambda: ex.resolve(10))

        ex.equal(0).and_less_than(1) .or_equal(2).and_greater_than(1)
        ex.resolve(0)
        ex.equal(0).and_less_than(1) .or_equal(2).and_greater_than(1)
        ex.resolve(2)

    def test_negation(self):
        ex = Expectation(deferred=True)

        ex.not_equal(3)
        ex.resolve(0)
        ex.NOT_equal(3)
        self.assertRaises(AssertionError, lambda: ex.resolve(3))

        ex.not_equal(3).and_not_equal(0)
        ex.resolve(1)
        ex.not_equal(3).and_Not_equal(0)
        self.assertRaises(AssertionError, lambda: ex.resolve(0))
        ex.not_equal(3).and_Not_equal(0)
        self.assertRaises(AssertionError, lambda: ex.resolve(3))

        ex.less_than(3).but_not_equal(2)
        ex.resolve(1)
        ex.less_than(3).But_Not_equal(2)
        self.assertRaises(AssertionError, lambda: ex.resolve(2))

    def test_no_matcher(self):
        ex = Expectation(deferred=True)

        ex.less_than(1).Or(3)
        ex.resolve(2)

        ex.less_than(1).And(3)
        ex.resolve(0)

