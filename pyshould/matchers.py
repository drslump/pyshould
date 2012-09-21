"""
Defines the registry of matchers and the standard set of matchers
"""

import re
import hamcrest as hc
from difflib import get_close_matches
from hamcrest.core.base_matcher import BaseMatcher

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"


# Words to ignore when looking up matchers
IGNORED_WORDS = ['should', 'to', 'be', 'a', 'an', 'is', 'the', 'as']

# Map of registered matchers as alias:callable
matchers = {}
# Map of normalized matcher aliases as normalized:alias
normalized = {}


class ContextManagerResult(object):
    """ When an expression is used in a `with` statement we capture the params
        in the __exit__ method of the expression context managet with this class,
        this allows to pass it to the matchers as the value to test, which is mostly
        useful for the raise/throw one.
    """
    def __init__(self, type_, value, trace):
        self.exc_type = type_
        self.exc_value = value
        self.trace = trace

    def __str__(self):
        """ Provide a suitable description of the exception for AnyOf/AllOf matchers """
        return repr(self.exc_value)


def register(matcher, *aliases):
    """ Register a matcher associated to one or more aliases. Each alias
        given is also normalized.
    """
    for alias in aliases:
        matchers[alias] = matcher
        # Map a normalized version of the alias
        norm = normalize(alias)
        normalized[norm] = alias
        # Map a version without snake case
        norm = norm.replace('_', '')
        normalized[norm] = alias


def unregister(matcher):
    """ Unregister a matcher (or alias) from the registry
    """

    # If it's a string handle it like an alias
    if isinstance(matcher, basestring) and matcher in matchers:
        matcher = matchers[matcher]

    # Find all aliases associated to the matcher
    aliases = [k for k, v in matchers.iteritems() if v == matcher]
    for alias in aliases:
        del matchers[alias]
        # Clean up the normalized versions
        norms = [k for k, v in normalized.iteritems() if v == alias]
        for norm in norms:
            del normalized[norm]

    return len(aliases) > 0


def normalize(alias):
    """ Normalizes an alias by removing adverbs defined in IGNORED_WORDS
    """
    # Convert from CamelCase to snake_case
    alias = re.sub(r'([a-z])([A-Z])', r'\1_\2', alias)
    # Ignore words
    words = alias.lower().split('_')
    words = filter(lambda w: w not in IGNORED_WORDS, words)
    return '_'.join(words)


def lookup(alias):
    """ Tries to find a matcher callable associated to the given alias. If
    an exact match does not exists it will try normalizing it and even
    removing underscores to find one.
    """

    if alias in matchers:
        return matchers[alias]
    else:
        norm = normalize(alias)
        if norm in normalized:
            alias = normalized[norm]
            return matchers[alias]

    # Check without snake case
    if -1 != alias.find('_'):
        norm = normalize(alias).replace('_', '')
        return lookup(norm)

    return None


def suggest(alias, max=3, cutoff=0.5):
    """ Suggest a list of aliases which are similar enough
    """

    aliases = matchers.keys()
    similar = get_close_matches(alias, aliases, n=max, cutoff=cutoff)

    return similar


# Matchers should be defined with verbose aliases to allow the use of
# natural english where possible. When looking up a matcher common adverbs
# like 'to', 'be' or 'is' are ignored in the comparison.
register(hc.equal_to,
         'be_equal_to', 'be_equals_to', 'be_eql_to', 'be_eq_to')
register(hc.instance_of,
         'be_an_instance_of', 'be_a', 'be_an')
register(hc.same_instance,
         'be_the_same_instance_as', 'be_the_same_as', 'be')

register(hc.has_entry,
         'have_the_entry', 'contain_the_entry')
register(hc.has_entries,
         'have_the_entries', 'contain_the_entries')
register(hc.has_key,
         'have_the_key', 'contain_the_key')
register(hc.has_value,
         'have_the_value', 'contain_the_value')
register(hc.is_in,
         'be_in', 'be_into', 'be_contained_in')
register(hc.has_item,
         'have_the_item', 'contain_the_item')
register(hc.has_items,
         'have_the_items', 'contain_the_items')
register(hc.contains_inanyorder,
         'have_in_any_order', 'contain_in_any_order')
register(hc.contains,
         'have', 'contain')
register(hc.only_contains,
         'have_only', 'contain_only')
register(hc.close_to,
         'be_close_to')
register(hc.greater_than,
         'be_greater_than', 'be_gt')
register(hc.greater_than_or_equal_to,
         'be_greater_than_or_equal_to', 'be_ge')
register(hc.less_than,
         'be_less_than', 'be_lt')
register(hc.less_than_or_equal_to,
         'be_less_than_or_equal_to', 'be_le')
register(hc.has_length,
         'have_length')
register(hc.has_property,
         'have_the_property', 'contain_the_property')
register(hc.has_string,
         'have_the_string', 'contain_the_string')
register(hc.equal_to_ignoring_case,
         'be_equal_to_ignoring_case')
register(hc.equal_to_ignoring_whitespace,
         'be_equal_to_ignoring_whitespace')
#register(hc.contains_string, 'have_the_string', 'contain_the_string')
register(hc.ends_with,
         'end_with')
register(hc.starts_with,
         'start_with', 'begin_with')
register(hc.anything,
         'be_anything')


class TypeMatcher(BaseMatcher):
    def _matches(self, item):
        return isinstance(item, self.__class__.types)

    def describe_to(self, description):
        description.append_text(self.__class__.expected)

    def describe_mismatch(self, item, description):
        description.append_text('was a %s ' % item.__class__.__name__)
        description.append_description_of(item)

    @classmethod
    def __call__(cls, *args, **kwargs):
        return cls()


class IsInteger(TypeMatcher):
    types = (int, long)
    expected = 'an integer'


class IsFloat(TypeMatcher):
    types = float
    expected = 'a float'


class IsComplex(TypeMatcher):
    types = complex
    expected = 'a complex number'


class IsNumeric(TypeMatcher):
    types = (int, long, float, complex)
    expected = 'a numeric type'


class IsString(TypeMatcher):
    types = basestring
    expected = 'a string'


class IsStr(TypeMatcher):
    types = str
    expected = 'a str'


class IsUnicode(TypeMatcher):
    types = unicode
    expected = 'a unicode string'


class IsByteArray(TypeMatcher):
    types = 'bytearray'
    expected = 'a bytearray'


class IsBuffer(TypeMatcher):
    types = 'buffer'
    expected = 'a buffer'


class IsXrange(TypeMatcher):
    types = 'xrange'
    expected = 'an xrange'


class IsDict(TypeMatcher):
    types = dict
    expected = 'a dict'


class IsList(TypeMatcher):
    types = list
    expected = 'a list'


class IsTuple(TypeMatcher):
    types = tuple
    expected = 'a tuple'


class IsSet(TypeMatcher):
    types = set
    expected = 'a set'


class IsFrozenSet(TypeMatcher):
    types = frozenset
    expected = 'a frozenset'


class IsFunction(TypeMatcher):
    import types
    types = types.FunctionType
    expected = 'a function'


class IsBool(TypeMatcher):
    types = bool
    expected = 'a bool'


class IsClass(BaseMatcher):
    def _matches(self, item):
        import inspect
        return inspect.isclass(item)

    def describe_to(self, desc):
        desc.append_text('a class')


register(IsInteger, 'be_an_integer', 'be_an_int')
register(IsFloat, 'be_a_float')
register(IsComplex, 'be_a_complex_number', 'be_a_complex')
register(IsNumeric, 'be_numeric')
register(IsString, 'be_a_string')
register(IsStr, 'be_a_str')
register(IsUnicode, 'be_an_unicode_string', 'be_an_unicode')
register(IsByteArray, 'be_a_bytearray', 'be_a_byte_array')
register(IsBuffer, 'be_a_buffer')
register(IsXrange, 'be_an_xrange')
register(IsDict, 'be_a_dictionary', 'be_a_dict')
register(IsList, 'be_a_list', 'be_an_array')
register(IsTuple, 'be_a_tuple')
register(IsSet, 'be_a_set')
register(IsFrozenSet, 'be_a_frozenset', 'be_a_frozen_set')
register(IsFunction, 'be_a_function', 'be_a_func')
register(IsBool, 'be_a_boolean', 'be_a_bool')
register(IsClass, 'be_a_class')


class IsIterable(BaseMatcher):
    """ Checks if a value is iterable """
    def _matches(self, item):
        try:
            iter(item)
            return True
        except TypeError:
            return False

    def describe_to(self, description):
        description.append_text('an iterable value')

register(IsIterable, 'be_an_iterable')


class IsCallable(BaseMatcher):
    """ Check if a value is callable """
    def _matches(self, item):
        return hasattr(item, '__call__')

    def describe_to(self, desc):
        desc.append_text('a callable value')

register(IsCallable, 'be_callable', 'be_a_callable_value', 'can_be_called')


class IsNone(BaseMatcher):
    """ Check if a value is None """
    def _matches(self, item):
        return True if item is None else False

    def describe_to(self, desc):
        desc.append_text('a None')

register(IsNone, 'be_none', 'be_a_none_value')


class IsTrue(BaseMatcher):
    """ Check if a value is True """
    def _matches(self, item):
        return item is True

    def describe_to(self, desc):
        desc.append_text('a True')


class IsFalse(BaseMatcher):
    """ Check if a value is False """
    def _matches(self, item):
        return item is False

    def describe_to(self, desc):
        desc.append_text('a False')


class IsTruthy(BaseMatcher):
    """ Check if a value is truthy """
    def _matches(self, item):
        return True if item else False

    def describe_to(self, desc):
        desc.append_text('a truthy value')


class IsFalsy(BaseMatcher):
    """ Check if a value is falsy """
    def _matches(self, item):
        return True if not item else False

    def describe_to(self, desc):
        desc.append_text('a falsy value')

register(IsTrue, 'be_true')
register(IsFalse, 'be_false')
register(IsTruthy, 'be_a_truthy_value', 'be_truthy')
register(IsFalsy, 'be_a_falsy_value', 'be_falsy')


class RaisesError(BaseMatcher):
    """ Checks if calling the value raises an error """

    def __init__(self, expected=None, message=None, regex=None):
        self.expected = expected
        self.message = message
        self.regex = regex
        self.thrown = None

    def _matches(self, item):
        self.thrown = None
        try:
            # support passing a context manager result
            if isinstance(item, ContextManagerResult):
                if item.exc_type is not None:
                    raise item.exc_value
            # support passing arguments by feeding a tuple instead of a callable
            elif not callable(item) and getattr(item, '__getitem__', False):
                item[0](*item[1:])
            else:
                item()

            return False
        except self.expected:
            return True
        except Exception as e:
            self.thrown = e
            if self.message:
                return self.message == str(e)
            elif self.regex:
                return re.match(self.regex, str(e)) is not None

            return self.expected is None

    def describe_to(self, desc):
        if self.thrown and self.message:
            desc.append_text('to raise an exception with message "%s"' % self.message)
        elif self.thrown and self.regex:
            desc.append_text('to raise an exception matching /%s/' % self.regex)
        else:
            desc.append_text('to raise an exception')
            if self.expected:
                try:
                    exps = map(lambda(x): x.__name__, self.expected)
                except:
                    exps = [self.expected.__name__]
                desc.append_text(' of type <%s>' % '>, <'.join(exps))

    def describe_mismatch(self, item, desc):
        if self.thrown:
            desc.append_text('was ')
            desc.append_text('<%s>' % self.thrown.__class__.__name__)
            if self.message or self.regex:
                desc.append_text(' "%s"' % str(self.thrown))
        else:
            desc.append_text('no exception was raised')

register(RaisesError,
         'raise_an_error', 'raise_an_exception',
         'raises_an_error', 'raises_an_exception', 'raises', 'raise',
         'throw_an_error', 'throw_an_exception',
         'throws_an_error', 'throws_an_exception', 'throws', 'throw')


from copy import deepcopy


class Changes(BaseMatcher):
    """ Checks if calling a value changes something """

    def __init__(self, watch):
        self.watch = watch
        self.before = None
        self.after = None
        self.changed = False

    def _matches(self, item):
        # support passing arguments by feeding a tuple instead of a callable
        if not callable(item) and getattr(item, '__getitem__', False):
            func = item[0]
            params = item[1:]
        else:
            func = item
            params = []

        try:
            before = self.watcher()
        except TypeError:
            before = self.watcher

        # keep a snapshot of the value in case it's mutable
        self.before = deepcopy(before)

        func(*params)

        try:
            self.after = self.watcher()
        except TypeError:
            self.after = self.watcher

        try:
            hc.assert_that(self.after, hc.equal_to(self.before))
            self.changed = False
        except AssertionError:
            self.changed = True

        return self.changed

    def describe_to(self, desc):
        desc.append_text('change something')

    def describe_mismatch(self, item, desc):
        # To support its proper use when negated we need to check if
        # the values actually changed or not
        if self.changed:
            desc.append_text('did change from ') \
                .append_value(self.before) \
                .append_text(' to ') \
                .append_value(self.after)
        else:
            desc.append_text('it didn\'t change from ') \
                .append_value(self.before)

register(Changes,
         'change', 'changes', 'modify', 'modifies')
