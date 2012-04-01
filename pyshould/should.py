import hamcrest as hc
from .matchers import lookup, suggest

class Should(object):
    """
    Represents an expectation allowing to configure it with matchers and
    finally resolving it.
    """

    def __init__(self, value=None, deferred=False, description=None):
        self.value = value
        self.deferred = deferred
        self.description = description
        self.matchers = []

    def reset(self):
        """Resets the state of the expectation"""
        self.matchers = []
        self.description = None

    def __ror__(self, lvalue):
        """
        Evaluate against the left hand side of the OR (pipe) operator. Since in
        Python this operator has a fairly low precedence this method will be
        called once the whole right hand side has been evaluated.
        """
        self.resolve(lvalue)
        return self

    def resolve(self, value = None):
        """Resolve the current set of matchers against the supplied value"""

        # More than one matcher is combined with an AND
        if len(self.matchers) > 1:
            matcher = hc.all_of(*self.matchers)
        else:
            matcher = self.matchers.pop()

        # If a description has been given include it in the matcher
        if self.description:
            matcher = hc.described_as(self.description, matcher)

        try:
            self.assertion(matcher, value)
        except AssertionError as ex:
            # By re-raising here the exception we reset the traceback
            raise ex
        finally:
            # Reset the state of the object so we can use it again
            self.reset()


    def assertion(self, matcher, value):
        """
        Perform the actual assertion for the given matcher and value. Override
        this method to apply a special configuration when performing the assertion.
        """
        hc.assert_that(value, matcher)

    def find_matcher(self, alias):
        """
        Finds a matcher based on the given alias or raises an error if no
        matcher could be found.
        """
        matcher = lookup(alias)
        if not matcher:
            msg = 'Matcher "%s" not found' % alias

            # Try to find similarly named matchers to help the user
            similar = suggest(alias, max=3, cutoff=0.5)
            if len(similar) > 1:
                last = similar.pop()
                msg += '. Perhaps you meant to use %s or %s?' % (', '.join(similar), last)
            elif len(similar) > 0:
                msg += '. Perhaps you meant to use %s?' % similar.pop()

            raise KeyError(msg)

        return matcher

    def described_as(self, description, *args):
        """
        Specify a custom message for the matcher
        """
        self.description = description.format(*args)
        return self 

    def desc(self, description, *args):
        """ Just an alias to described_as """
        return self.described_as(description, *args)


    def __getattr__(self, name):
        """
        Overload property access to interpret them as matchers.
        """
        matcher = self.find_matcher(name)
        self.matchers.append(matcher)

        return self

    def __call__(self, *args, **kwargs):
        """
        Execute the matcher just registered by __getattr__ passing any given
        arguments. If we're in deferred mode we don't resolve the matcher yet,
        it'll be done in the __ror__ overload.
        """

        if not len(self.matchers):
            raise TypeError('No matchers set. Usage: <value> | should.<matcher>(<expectation>)')

        # Replace the last matcher by the result of executing it
        matcher = self.matchers.pop()
        matcher = matcher(*args)
        self.matchers.append(matcher)

        if not self.deferred:
            self.resolve(self.value)

        return self


class ShouldNot(Should):
    """
    Negates the result of the matcher
    """
    def assertion(self, matcher, value):
        hc.assert_that(value, hc.is_not(matcher))

class ShouldAny(Should):
    """
    Succeeds if any of the items in an iterable value passes the matcher
    """
    def assertion(self, matcher, value):
        hc.assert_that(value, hc.has_item(matcher))

class ShouldAll(Should):
    """
    Succeeds if all of the items in an iterable value pass the matcher
    """
    def assertion(self, matcher, value):
        hc.assert_that(value, hc.only_contains(matcher))

class ShouldNone(Should):
    """
    Succeeds if none of the items in an iterable value pass the matcher
    """
    def assertion(self, matcher, value):
        hc.assert_that(value, hc.is_not(hc.has_item(matcher)))


