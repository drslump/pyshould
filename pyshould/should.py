import hamcrest as hc
from difflib import get_close_matches

class Matchers:

    IGNORED_KEYWORDS = ['should', 'to', 'be', 'a', 'an', 'is', 'the', 'as']

    matchers = {}
    normalized = {}

    @classmethod
    def register(cls, matcher, *aliases):
        """
        Register a matcher associated to one or more aliases
        """
        # For each alias given register the matcher
        for alias in aliases:
            cls.matchers[alias] = matcher
            # Map a normalized version of the alias
            normalized = cls.normalize(alias)
            cls.normalized[normalized] = alias

    @classmethod
    def normalize(cls, alias):
        """
        Normalizes an alias by removing adverbs
        """
        words = alias.lower().split('_')
        words = filter(lambda(x): x not in cls.IGNORED_KEYWORDS, words)
        return '_'.join(words)

    @classmethod
    def find(cls, alias):
        matcher = None
        # First we search in the registered aliases
        if alias in cls.matchers:
            return cls.matchers[alias]
        else:
            # Otherwise we try normalizing it to find a matcher
            normalized = cls.normalize(alias)
            if normalized in cls.normalized:
                alias = cls.normalized[normalized]
                return cls.matchers[alias]

        return None

    @classmethod
    def list(cls):
        return cls.matchers.keys()


class Should(object):

    def __init__(self, value=None, deferred=False):
        self.value = value
        self.deferred = deferred

    def __ror__(self, lvalue):
        """
        Evaluate against the left hand side of the OR (pipe) operator. Since in
        Python this operator has a fairly low precedence this method will be
        called once the whole right hand side has been evaluated.
        """
        self.resolve(lvalue)
        return self

    def resolve(self, value):
        try:
            self.assertion(value, self.matcher)
        except AssertionError as ex:
            # By re-raising here the exception we reset the traceback
            raise ex

    def assertion(self, value, matcher):
        hc.assert_that(value, matcher)

    def match(self, alias):
        matcher = Matchers.find(alias)
        if not matcher:
            msg = 'Matcher "%s" not found' % alias

            # Try to find similarly named matchers to help the user
            aliases = Matchers.list()
            similar = get_close_matches(alias, aliases, n=3, cutoff=0.3)
            if len(similar) > 1:
                last = similar.pop()
                msg += '. Perhaps you meant to use %s or %s?' % (', '.join(similar), last)
            elif len(similar) > 0:
                msg += '. Perhaps you meant to use %s' % similar.pop()

            raise NameError(msg)

        return matcher

    def __getattr__(self, name):
        """
        Overload property access to interpret them as matchers.
        By returning the matcher wrapped in a function we can assign the result
        to the internal matcher property and actually return this same object
        allowing the __ror__ to be finally evaluated.
        """
        matcher = self.match(name)

        if not self.deferred:
            return Callable(self, matcher)

        def wrapper(*args):
            self.matcher = matcher(*args)
            return self

        return wrapper

class ShouldAny(Should):

    def assertion(self, value, matcher):
        hc.assert_that(value, hc.has_item(matcher))

class ShouldAll(Should):

    def assertion(self, value, matcher):
        hc.assert_that(value, hc.only_contains(matcher))


class ShouldNone(Should):

    def assertion(self, value, matcher):
        hc.assert_that(value, hc.is_not(hc.has_item(matcher)))

class ShouldNot(Should):

    def assertion(self, value, matcher):
        hc.assert_that(value, hc.is_not(matcher))


class Callable(object):

    def __init__(self, should, matcher):
        self.should = should
        self.matcher = matcher

    def __call__(self, *args, **kwargs):
        self.should.matcher = self.matcher(*args)
        self.should.resolve(self.should.value)


# Create instances to be used by default
should = Should(deferred=True)
should_not = ShouldNot(deferred=True)
should_all = ShouldAll(deferred=True)
should_any = ShouldAny(deferred=True)
should_none = ShouldNone(deferred=True)


def it(value):
    return Should(value)

def any(value):
    return ShouldAny(value)
any_of = any

def all(value):
    return ShouldAll(value)
all_of = all

def none(value):
    return ShouldNone(value)
none_of = none


# Matchers should be defined with verbose aliases to allow the use of
# natural english where possible. When looking up a matcher common adverbs
# like 'to', 'be' or 'is' are ignored in the comparison.

Matchers.register(hc.equal_to,
    'be_equal_to', 'be_eql_to', 'be_eq_to')
Matchers.register(hc.instance_of,
    'be_an_instance_of', 'be_a', 'be_an')
Matchers.register(hc.same_instance,
    'be_the_same_instance_as', 'be_the_same_as', 'be')

Matchers.register(hc.has_entry,
    'have_the_entry', 'contain_the_entry')
Matchers.register(hc.has_entries,
    'have_the_entries', 'contain_the_entries')
Matchers.register(hc.has_key,
    'have_the_key', 'contain_the_key')
Matchers.register(hc.has_value,
    'have_the_value', 'contain_the_value')
Matchers.register(hc.is_in,
    'be_in')
Matchers.register(hc.has_item,
    'have_the_item', 'contain_the_item')
Matchers.register(hc.has_items,
    'have_the_items', 'contain_the_items')
Matchers.register(hc.contains_inanyorder,
    'have_in_any_order', 'contain_in_any_order')
Matchers.register(hc.contains,
    'have', 'contain')
Matchers.register(hc.only_contains,
    'have_only', 'contain_only')
Matchers.register(hc.close_to,
    'be_close_to')
Matchers.register(hc.greater_than,
    'be_greater_than')
Matchers.register(hc.greater_than_or_equal_to,
    'be_greater_than_or_equal_to')
Matchers.register(hc.less_than,
    'be_less_than')
Matchers.register(hc.less_than_or_equal_to,
    'be_less_than_or_equal_to')
Matchers.register(hc.has_length,
    'have_length')
Matchers.register(hc.has_property,
    'have_the_property', 'contain_the_property')
Matchers.register(hc.has_string,
    'have_the_string', 'contain_the_string')
Matchers.register(hc.equal_to_ignoring_case,
    'be_equal_to_ignoring_case')
Matchers.register(hc.equal_to_ignoring_whitespace,
    'be_equal_to_ignoring_whitespace')
#Matchers.register(hc.contains_string, 'have_the_string', 'contain_the_string')
Matchers.register(hc.ends_with,
    'end_with')
Matchers.register(hc.starts_with,
    'start_with', 'begin_with')

