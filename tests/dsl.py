import unittest2
from pyshould import *
from pyshould import dsl
from pyshould import Expectation


class DslTestCase(unittest2.TestCase):
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
        self.assertRaises(AssertionError, lambda: [0, 1] | should.equal(0))

    def test_should_any(self):
        self.assertRaises(AssertionError, lambda: [0, 1] | should.equal(2))

    def test_should_none(self):
        self.assertRaises(AssertionError, lambda: [0, 1] | should.equal(1))

    def test_it(self):
        self.assertRaises(AssertionError, lambda: it(0).equal(1))

    def test_all_of(self):
        self.assertRaises(AssertionError, lambda: all_of([1, 2]).equal(1))
        self.assertRaises(AssertionError, lambda: all_of((1, 2)).equal(1))
        self.assertRaises(AssertionError, lambda: all_of(1, 2).equal(1))

    def test_any_of(self):
        self.assertRaises(AssertionError, lambda: any_of([2, 2]).equal(1))
        self.assertRaises(AssertionError, lambda: any_of((2, 2)).equal(1))
        self.assertRaises(AssertionError, lambda: any_of(2, 2).equal(1))

    def test_none_of(self):
        self.assertRaises(AssertionError, lambda: none_of([2, 1]).equal(1))
        self.assertRaises(AssertionError, lambda: none_of((2, 1)).equal(1))
        self.assertRaises(AssertionError, lambda: none_of(2, 1).equal(1))

    def test_context_manager(self):
        def fail_not_thrown():
            with should.throw:
                pass
        self.assertRaises(AssertionError, fail_not_thrown)

        def fail_thrown():
            with should.not_throw:
                raise KeyError('foo')
        self.assertRaises(AssertionError, fail_thrown)

        def nested_expression_ok():
            with should.throw(TypeError):
                1 | should.equal(1)
        self.assertRaisesRegexp(AssertionError, 'TypeError', nested_expression_ok)

        def nested_expression_fail():
            with should.throw(TypeError):
                1 | should.equal(2)
        self.assertRaisesRegexp(AssertionError, '<2>', nested_expression_fail)

        with should.throw(TypeError):
            raise TypeError('foo')

        with should.not_throw(TypeError):
            raise KeyError('foo')

        with should.throw:
            raise KeyError('foo')

        with should.not_throw:
            pass

        class FooError(Exception):
            def __init__(self, foo, msg=None):
                if not foo:
                    raise ValueError('foo is not defined')

        with should.throw(FooError):
            raise FooError(10)

    def test_expect_throw_non_empty_constructor_exception(self):
        with should.throw(NonEmptyConstructorException):
            raise NonEmptyConstructorException([])

    def test_expect_throw_str_exceptions(self):
        with should.throw(KeyError):
            raise KeyError()

        with should.throw(KeyError):
            object = {}
            object['non-existing-key']

    def test_callback_matcher(self):
        1 | should.pass_callback(lambda x: x == 1)

    def test_callback_matcher_nested_expectation(self):
        1 | should.pass_callback(lambda x: x | should.eq(1))

    def test_matcher_composition(self):
        d = {'foo': 'bar'}
        d | should.have_value(should.eq('bar'))
        d | should.have_entry('foo', should.eq('baz').or_eq('bar'))
        d | should.have_key('foo').and_have_value(should.eq('bar'))

        self.assertRaises(
            AssertionError,
            lambda: d | should.have_entry('foo', should.eq('baz'))
        )

    def test_configuring_matchers(self):
        m1 = should.eq(1)
        m2 = should.eq(2)
        m1.resolve(1)
        m2.resolve(2)

        m1 = should.be_true
        m2 = should.be_false
        m1.resolve(True)
        m2.resolve(False)


class NonEmptyConstructorException(Exception):

    parameter = []

    @property
    def text(self):
        return self.parameter

    def __init__(self, parameter, message=None):
        if parameter is None:
            raise TypeError("parameter could not be None")

        self.parameter = parameter
        self.message = message

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Missing fields: %s' % (self.parameter)            
