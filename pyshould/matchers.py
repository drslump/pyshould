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
# Help messages associated to matchers
helpmatchers = {}


# All textual representation types in Python 2/3
try:
    text_types = (basestring, str, unicode)  # python 2
except NameError:
    text_types = (str,)


class ContextManagerResult(object):
    """ When an expression is used in a `with` statement we capture the params
        in the __exit__ method of the expression context manager with this class,
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
    docstr = matcher.__doc__ if matcher.__doc__ is not None else ''
    helpmatchers[matcher] = docstr.strip()

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
    if isinstance(matcher, six.string_types) and matcher in matchers:
        matcher = matchers[matcher]

    # Find all aliases associated to the matcher
    aliases = [k for k, v in matchers.iteritems() if v == matcher]
    for alias in aliases:
        del matchers[alias]
        # Clean up the normalized versions
        norms = [k for k, v in normalized.iteritems() if v == alias]
        for norm in norms:
            del normalized[norm]

    # Remove help docstring
    if matcher in helpmatchers:
        del helpmatchers[matcher]

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


def aliases():
    """ Obtain the list of aliases """
    return list(matchers.keys())


def alias_help(alias):
    """ Get help for the given alias """
    matcher = lookup(alias)
    if not matcher:
        return None
    return helpmatchers.get(matcher)


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
         'be_greater_than', 'be_greater', 'be_gt',
         'be_above', 
         'be_more_than', 'be_more')
register(hc.greater_than_or_equal_to,
         'be_greater_than_or_equal_to', 'be_greater_or_equal', 'be_ge', 
         'be_more_than_or_equal', 'be_more_or_equal' 
         'be_at_least')
register(hc.less_than,
         'be_less_than', 'be_less', 'be_lt', 'be_below')
register(hc.less_than_or_equal_to,
         'be_less_than_or_equal_to', 'be_less_or_equal', 'be_le', 
         'be_at_most')
register(hc.has_length,
         'have_length', 'have_len')
register(hc.has_property,
         'have_the_property', 'contain_the_property', 'have_the_prop', 'contain_the_prop')
register(hc.has_string,
         'have_the_string', 'contain_the_string')
register(hc.equal_to_ignoring_case,
         'be_equal_to_ignoring_case')
register(hc.equal_to_ignoring_whitespace,
         'be_equal_to_ignoring_whitespace')
register(hc.contains_string,
         'substr', 'have_the_substr', 'contain_the_substr',
         'substring', 'have_the_substring', 'contain_the_substring')
register(hc.ends_with,
         'end_with')
register(hc.starts_with,
         'start_with', 'begin_with')
register(hc.anything,
         'be_anything', 'be_any')


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
    """ Check if the value is an integer """
    try:
        types = (int, long)
    except:
        types = (int)  # Python 3
    expected = 'an integer'


class IsFloat(TypeMatcher):
    """ Check if the value is a float """
    types = float
    expected = 'a float'


class IsComplex(TypeMatcher):
    """ Check if the value is a complex number """
    types = complex
    expected = 'a complex number'


class IsNumeric(TypeMatcher):
    """ Check if the value is a numeric type """
    try:
        types = (int, long, float, complex)  # python 2
    except NameError:
        types = (int, float, complex)

    expected = 'a numeric type'


class IsString(TypeMatcher):
    """ Check if the value is a string """
    types = text_types
    expected = 'a string'


class IsStr(TypeMatcher):
    """ Check if the value is a str """
    try:
        types = (basestring, str)  # python 2
    except NameError:
        types = str

    expected = 'a str'


class IsUnicode(TypeMatcher):
    """ Check if the value is an unicode string """
    try:
        types = unicode  # python 2
    except NameError:
        types = str

    expected = 'a unicode string'


class IsBinary(TypeMatcher):
    """ Check if value is a binary string """
    try:
        types = bytes  # python 3
    except NameError:
        types = str

    expected = 'a binary string'


class IsByteArray(TypeMatcher):
    """ Check if the value is a bytearray """
    types = bytearray
    expected = 'a bytearray'


class IsDict(TypeMatcher):
    """ Check if the value is a dict """
    types = dict
    expected = 'a dict'


class IsList(TypeMatcher):
    """ Check if the value is a list """
    types = list
    expected = 'a list'


class IsTuple(TypeMatcher):
    """ Check if the value is a tuple """
    types = tuple
    expected = 'a tuple'


class IsSet(TypeMatcher):
    """ Check if the value is a set """
    types = set
    expected = 'a set'


class IsFrozenSet(TypeMatcher):
    """ Check if the value is a frozenset """
    types = frozenset
    expected = 'a frozenset'


class IsBool(TypeMatcher):
    """ Check if the value is a bool """
    types = bool
    expected = 'a bool'


class IsFunction(TypeMatcher):
    """ Check if the value is a function """
    import types
    types = types.FunctionType
    expected = 'a function'


class IsGenerator(BaseMatcher):
    """ Checks if the value is a generator function """
    def _matches(self, item):
        import inspect
        return inspect.isgeneratorfunction(item)

    def describe_to(self):
        desc.append_text('a generator function')


class IsClass(BaseMatcher):
    """ Check if the value is a class """
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
register(IsUnicode, 'be_a_binary_string', 'be_a_binary')
register(IsByteArray, 'be_a_bytearray', 'be_a_byte_array')
register(IsDict, 'be_a_dictionary', 'be_a_dict')
register(IsList, 'be_a_list', 'be_an_array')
register(IsTuple, 'be_a_tuple')
register(IsSet, 'be_a_set')
register(IsFrozenSet, 'be_a_frozenset', 'be_a_frozen_set')
register(IsFunction, 'be_a_function', 'be_a_func')
register(IsBool, 'be_a_boolean', 'be_a_bool')
register(IsGenerator, 'be_a_generator')
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
register(IsTruthy, 'be_a_truthy_value', 'be_truthy', 'be_ok')
register(IsFalsy, 'be_a_falsy_value', 'be_falsy', 'be_ko')


class IsEmpty(BaseMatcher):
    """ Check if a value is empty """
    def _matches(self, item):
        try:
            return not bool(len(item))
        except:
            return False

    def describe_to(self, desc):
        desc.append_text('an empty value')

    def describe_mismatch(self, item, desc):
        try:
            l = len(item)
            desc.append_text('has {0} elements'.format(l))
        except:
            desc.append_value(item)
            desc.append_text(' does not have a length')

register(IsEmpty, 'be_empty')


class RaisesError(BaseMatcher):
    """ Checks if calling the value raises an error """

    def __init__(self, expected=None, message=None, regex=None):
        self.expected = expected
        self.message = message
        self.regex = regex
        self.thrown = None

    def _matches(self, item):
        # support passing a context manager result
        if isinstance(item, ContextManagerResult):
            # Python <2.7 may provide a non exception value
            if isinstance(item.exc_value, Exception):
                self.thrown = item.exc_value
            elif item.exc_type is not None:
                self.thrown = item.exc_type(*item.exc_value)
            else:
                return False
        else:
            try:
                # support passing arguments by feeding a tuple instead of a callable
                if not callable(item) and getattr(item, '__getitem__', False):
                    item[0](*item[1:])
                else:
                    item()
                return False
            except:
                # This should capture any kind of raised value
                import sys
                self.thrown = sys.exc_info()[1]

        # Fail if we have defined an expected error type
        if self.expected and not isinstance(self.thrown, self.expected):
            return False

        # Apply message filters
        if self.message:
            return self.message == str(self.thrown)
        elif self.regex:
            return re.match(self.regex, str(self.thrown))

        return True

    def describe_to(self, desc):
        if self.thrown and self.message:
            desc.append_text('to raise an exception with message "%s"' % self.message)
        elif self.thrown and self.regex:
            desc.append_text('to raise an exception matching /%s/' % self.regex)
        else:
            desc.append_text('to raise an exception')
            if self.expected:
                try:
                    exps = map(lambda x: x.__name__, self.expected)
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
        from copy import deepcopy
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


class Callback(BaseMatcher):
    """ Checks against an user supplied callback. The callback
        can should return True to indicate a successful match or
        False to indicate an unsuccessful one. 
    """

    def __init__(self, callback):
        self.callback = callback

    def _matches(self, item):
        self.error = None
        try:
            result = self.callback(item)
            # Returning an expectation assumes it's correct (no failure raised)
            from .expectation import Expectation
            return isinstance(result, Expectation) or bool(result)
        except AssertionError:
            # Just forward assertion failures
            raise
        except Exception as ex:
            self.error = str(ex)
            return False

    def describe_to(self, desc):
        desc.append_text('passses callback ')
        if isinstance(self.callback, type(lambda: None)) and self.callback.__name__ == '<lambda>':
            desc.append_text(self.callback.__name__)
        else:
            desc.append_text('{0}'.format(self.callback))

    def describe_mismatch(self, item, desc):
        if self.error:
            desc.append_text('gave an exception "%s"' % self.error)
        else:
            desc.append_text('returned False')


register(Callback,
         'callback', 'pass', 'pass_callback')


class MockCalled(BaseMatcher):
    """ Support for checking if mocks where called from the Mock library
    """
    def _matches(self, item):
        if not hasattr(item, 'called'):
            raise Exception('Mock object does not have a <called> attribute')
        return item.called

    def describe_to(self, desc):
        desc.append_text('called')

    def describe_mismatch(self, item, desc):
        if item.called:
            desc.append_text('was called')
        else:
            desc.append_text('was not called')

register(MockCalled, 'called', 'invoked')


class RegexMatcher(BaseMatcher):
    """ Checks against a regular expression """

    def __init__(self, regex, flags=0):
        self.regex = regex

        if isinstance(flags, text_types):
            self.flags = 0
            for ch in flags.upper():
                self.flags |= getattr(re, ch)
        else:
            self.flags = flags

    def _matches(self, item):
        # Make sure we are matching against a string
        hc.assert_that(item, IsString())
        
        match = re.search(self.regex, item, self.flags)
        return match is not None

    def describe_to(self, desc):
        desc.append_text('matching ')
        desc.append_text('/{0}/'.format(self.regex))

register(RegexMatcher, 'match', 'match_regex', 'match_regexp', 'be_matched_by')
