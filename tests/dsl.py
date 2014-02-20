try:
    import unittest2 as unittest  # Python 2.6
except:
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

    def test_match(self):
        "foo" | should.match('^\w+$')

    def test_match_flags(self):
        "FOO" | should.match('^[a-z]+$', 'i')

    def test_match_non_string(self):
        self.assertRaises(
            AssertionError,
            lambda: 10 | should.match('^\d+')
        )

    def test_callback_matcher(self):
        1 | should.pass_callback(lambda x: x == 1)

    def test_callback_matcher_nested_expectation(self):
        1 | should.pass_callback(lambda x: x | should.eq(1))

    def test_empty_matcher(self):
        [] | should.be_empty
        '' | should.be_empty
        {} | should.be_empty
        ['foo'] | should_not.be_empty
        'foo' | should_not.be_empty
        {'foo':'foo'} | should_not.be_empty

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

    def test_nested_matchers(self):
        d = dict(a='A', b='B', c='C')
        d | should.have_entries({
            'a': should.be_str.and_not_empty,
            'b': should.be_str,
            'c': should_not.eq('Z')
        })

    def test_nested_matchers_failure(self):
        d = dict(a='A', b='B', c='C')
        try:
            d | should.have_entries({
                'a': should.be_str.and_not_empty,
                'z': should.be_str,
                'c': should_not.eq('Z')
            })
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass

    def test_apply(self):
        import json
        d = '{"foo":"bar"}'

        d | should(json.loads).have_key('foo')

        should_json = should(json.loads)
        d | should_json.have_key('foo')
        '{"bar": 10}' | should_json.have_key('bar')

        try:
            d | should(json.loads).have_key('bar')
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass

    def test_apply_error(self):
        import json
        d = '{malformed}'

        try:
            d | should(json.loads).be_anything
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass

    def test_equality(self):
        m = should.be_int.and_eq(1)
        self.assertEqual(1, m)

        self.assertRaises(
            AssertionError,
            lambda: self.assertEqual(m, 2)
        )

    def test_inequality(self):
        m = should.be_int.and_eq(2)
        self.assertNotEqual(1, m)

        self.assertRaises(
            AssertionError,
            lambda: self.assertNotEqual(m, 2)
        )

    def test_mock(self):
        try:
            from unittest.mock import Mock  # Python 3.3
        except:
            try:
                from mock import Mock
            except:
                raise unittest.SkipTest('Mock library not available, skipping test')

        mock = Mock()
        mock(10, 1)

        mock | should.be_called
        self.assertRaises(
            AssertionError,
            lambda: mock | should.not_be_called
        )

        # Check it supports matchers in params
        mock.assert_called_with(should.any, should.less_than(3))
        self.assertRaises(
            AssertionError,
            lambda: mock.assert_called_with(should.any, should.greater_than(3))
        )

    def test_patch_mockito(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from pyshould import patch_mockito
            w | should.have_len(1)
            w[0].category | should.be(DeprecationWarning)
            

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
