import unittest
from pyshould import *
from pyshould.expect import expect, expect_all, expect_any, expect_none

class ExpectTestCase(unittest.TestCase):
    """ Simple tests for the expect based api """

    def test_expect(self):
        expect(1).to_equal(1)
        expect(1).to_not_equal(0)

    def test_expect_all(self):
        expect_all([1,2]).to_be_integer()
        expect_all(1, 2).to_be_integer()

    def test_expect_any(self):
        expect_any([1,2]).to_equal(2)
        expect_any(1,2).to_equal(2)

    def test_expect_none(self):
        expect_none([1,2]).to_equal(0)
        expect_none(1,2).to_equal(0)

    def test_expect_quantifiers(self):
        expect(all_of(1, 2)).to_be_integer()
        expect(any_of([1, 2])).to_eq(1)

