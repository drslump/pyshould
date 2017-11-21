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
            self.assertTrue(kw in globals(),
                            msg='keyword "%s" not found as global' % kw)
            self.assertTrue(kw in dir(dsl),
                            msg='keyword "%s" not found in dsl' % kw)

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

    def test_should_property(self):
        a = it(10)
        it(10).should.eq(10)
        it(10).should_not.eq(20)

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

        all_of([1, 2]) | should.be_int

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
        self.assertRaisesRegexp(AssertionError,
                                'TypeError', nested_expression_ok)

        def nested_expression_fail():
            with should.throw(TypeError):
                1 | should.equal(2)
        self.assertRaisesRegexp(AssertionError,
                                '<2>', nested_expression_fail)

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
        {'foo': 'foo'} | should_not.be_empty

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

    def test_class_has_props(self):
        d = type("CommentForm", (object,),
                 {'text': 'textvalue', 'author': 'the_author'})

        d | should.have_properties({
            'text': 'textvalue',
            'author': 'the_author',
        })

    def test_object_has_props(self):
        Cls = type("CommentForm", (object,), {'text': '', 'author': ''})
        d = Cls()
        d.text = 'textvalue'
        d.author = 'the_author'

        d | should.have_properties({
            'text': 'textvalue',
            'author': 'the_author',
        })

    def test_object_has_dynamic_props(self):
        Cls = type("CommentForm", (object,), {})
        d = Cls()
        d.added_text = 'textvalue'
        d.added_author = 'the_author'

        d | should.have_attrs({
            'added_text': 'textvalue',
            'added_author': should.be_a_string(),
        })

    def test_object_has_dynamic_props_with_kwargs(self):
        Cls = type("CommentForm", (object,), {})
        d = Cls()
        d.added_text = 'textvalue'
        d.added_author = 'the_author'

        d | should.have_attrs(added_text='textvalue',
                              added_author=should.be_a_string())

    def test_object_has_dynamic_props_with_non_existing_kwargs(self):
        Cls = type("CommentForm", (object,), {})
        d = Cls()
        d.added_text = 'textvalue'
        d.added_author = 'the_author'
        with self.assertRaises(AssertionError):
            d | should.have_attrs(added_text='textvalue',
                                  added_author=should.be_a_string(),
                                  fake='foo')

    def test_has_props_non_class(self):
        d = "fail"

        with self.assertRaises(AssertionError):
            d | should.have_properties({
                'text': should.be_a_string(),
                'author': 'the_author',
            })

    def test_old_style_class_has_props(self):
        class CommentForm:
            text_field = "textvalue"
            author_field = "the_author"

        d = CommentForm()

        d | should.have_properties({
            'text_field': 'textvalue',
            'author_field': 'the_author',
        })

    def test_datetime_type_check(self):
        from datetime import datetime

        datetime.utcnow() | should.be_a_date()

    def test_date_type_check(self):
        from datetime import date

        date.today() | should.be_a_date()

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

    def test_apply_all(self):
        import json
        d = ('{"bar": 10}', '{"bar": 20}')

        d | should_all(json.loads).have_key('bar')

        should_all_json = should_all(json.loads)
        d | should_all_json.have_key('bar')

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

    def test_equality_exception(self):
        # under the hood the equality for `should` should trigger an error
        (10 == should) | should.be_False
        (10 == should.equal) | should.be_False
        (10 != should) | should.be_True
        (10 != should.equal) | should.be_True

    def test_mock(self):
        try:
            from unittest.mock import Mock, patch  # Python 3.3
        except:
            try:
                from mock import Mock, patch
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

        # Check we can wrap it even when implementing __or__
        with patch.object(self, 'test_mock') as mock:
            it(mock) | should.not_be_called

    def test_patch_mockito(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from pyshould import patch_mockito
            w | should.have_len(1)
            w[0].category | should.be(DeprecationWarning)

    def test_compatibility_with_assert(self):

        assert 10 | should.be_less_than(20)

        try:
            assert 10 | should.be_greater_than(20)
            raise RuntimeError('Should not reach this point')
        except AssertionError:
            pass

    def test_repr_expr(self):
        expr = it(10)
        repr(expr) | should.be_a_string

        expr = it(10).should.be_an_int
        repr(expr) | should.be_a_string

        expr = it(10).should.eq(10)
        repr(expr) | should.be_a_string

    def test_repr_deferred_expr(self):
        repr(should.be_empty) | should.be_a_string

    def test_base_except(self):
        import sys
        with should.throw(SystemExit):
            sys.exit(66)

    def test_base_except_not_thrown(self):
        with should_not.throw(SystemExit):
            pass

    def test_wrap_value(self):
        it(10) | should.eq(10)

    def test_dumper(self):
        output = []
        mockdumper = dumper(reporter=output.append)

        data = {'foo': 'Foo', 'bar': 'Bar', 'baz': 'Baz'}
        data | should.eq({
            'foo': mockdumper(msg='this is foo'),
            'bar': mockdumper,
            'baz': mockdumper(should.start_with('B'), msg='BAZ!')
        })

        output.sort()
        output | should.eq([
            "'Bar'",
            "BAZ!: 'Baz'",
            "this is foo: 'Foo'",
        ])

    def test_contain_sparse_in_order(self):
        with self.assertRaises(AssertionError):
            [1, 4, 3, 3, 3, 6] | should.contain_sparse_in_order(
                should.eq(1), should.be_greater_than(7)
            )

        with self.assertRaises(AssertionError):
            [1, 4, 3, 3, 3, 8, 9] | should.contain_sparse_in_order(
                should.eq(1), should.be_greater_than(7)
            )

        with self.assertRaises(AssertionError):
            [9, 1] | should.contain_sparse_in_order(
                should.eq(1), should.be_greater_than(7)
            )

        with self.assertRaises(AssertionError):
            1 | should.contain_sparse_in_order(
                should.eq(1)
            )

        with self.assertRaises(AssertionError):
            [1] | should.contain_sparse_in_order(
                should.eq(1), should.be_greater_than(7)
            )

        [1, 4, 3, 3, 8, 6, 2] | should.contain_sparse_in_order(
            should.eq(1), should.be_greater_than(7)
        )

        [0, 1, 4, 3, 3, 8, 6, 2] | should.contain_sparse_in_order(
            should.eq(1), should.be_greater_than(7)
        )

        (i for i in range(9)) | should.contain_sparse_in_order(
            1, should.be_greater_than(7)
        )


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
