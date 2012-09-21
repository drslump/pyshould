"""
Defines the expectation class which is the basis for performing the assertions.
"""
import re
import hamcrest as hc

from .patched import IsNot
from .matchers import lookup, suggest, ContextManagerResult

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"


class OPERATOR:
    """ Define the set of coordination operators assigning to them a weight
        to indicate their precedence. Higher values take precedence over
        lower ones.
    """
    NOT = 20
    AND = 10
    OR = 5
    BUT = 1


class Expectation(object):
    """ Represents an expectation allowing to configure it with matchers and
        finally resolving it.
    """

    _contexts = []

    def __init__(self, value=None, deferred=False, description=None,
                 def_op=OPERATOR.AND, def_matcher='equal'):
        self.reset()
        self.value = value
        self.deferred = deferred
        self.description = description
        self.def_op = def_op
        self.def_matcher = def_matcher

    def reset(self):
        """ Resets the state of the expression """
        self.expr = []
        self.matcher = None
        self.last_matcher = None
        self.description = None

    def clone(self):
        """ Clone this expression """
        from copy import copy
        clone = copy(self)
        clone.expr = copy(self.expr)
        return clone

    def __ror__(self, lvalue):
        """ Evaluate against the left hand side of the OR (pipe) operator. Since in
            Python this operator has a fairly low precedence this method will usually
            be called once the whole right hand side of the expression has been evaluated.
        """
        self.resolve(lvalue)
        return self

    def resolve(self, value=None):
        """ Resolve the current expression against the supplied value """

        # If we still have an uninitialized matcher init it now
        if self.matcher:
            self._init_matcher()

        # Evaluate the current set of matchers forming the expression
        matcher = self._evaluate()

        # If a description has been given include it in the matcher
        if self.description:
            matcher = hc.described_as(self.description, matcher)

        try:
            self._assertion(matcher, value)

        except AssertionError as ex:
            # By re-raising here the exception we reset the traceback
            raise ex
        finally:
            # Reset the state of the object so we can use it again
            self.reset()

    def _assertion(self, matcher, value):
        """ Perform the actual assertion for the given matcher and value. Override
            this method to apply a special configuration when performing the assertion.
            If the assertion fails it should raise an AssertionError.
        """

        # To support the syntax `any_of(subject) | should ...` we check if the
        # value to check is an Expectation object and if it is we use the descriptor
        # protocol to bind the value's assertion logic to this expectation.
        if isinstance(value, Expectation):
            assertion = value._assertion.__get__(self, Expectation)
            assertion(matcher, value.value)
        else:
            hc.assert_that(value, matcher)

    def _evaluate(self):
        """ Converts the current expression into a single matcher, applying
            coordination operators to operands according to their binding rules
        """

        # Apply Shunting Yard algorithm to convert the infix expression
        # into Reverse Polish Notation. Since we have a very limited
        # set of operators and binding rules, the implementation becomes
        # really simple. The expression is formed of hamcrest matcher instances
        # and operators identifiers (ints).
        ops = []
        rpn = []
        for token in self.expr:
            if isinstance(token, (int, long)):
                while len(ops) and token <= ops[-1]:
                    rpn.append(ops.pop())
                ops.append(token)
            else:
                rpn.append(token)

        # Append the remaining operators
        while len(ops):
            rpn.append(ops.pop())

        # Walk the RPN expression to create AllOf/AnyOf matchers
        stack = []
        for token in rpn:
            if isinstance(token, (int, long)):
                # Handle the NOT case in a special way since it's unary
                if token == OPERATOR.NOT:
                    stack[-1] = IsNot(stack[-1])
                    continue

                # Our operators always need two operands
                if len(stack) < 2:
                    raise RuntimeError('Unable to build a valid expression. Not enough operands available.')

                # Check what kind of matcher we need to create
                if token == OPERATOR.OR:
                    matcher = hc.any_of(*stack[-2:])
                else:  # AND, BUT
                    matcher = hc.all_of(*stack[-2:])

                stack[-2:] = [matcher]
            else:
                stack.append(token)

        if len(stack) != 1:
            raise RuntimeError('Unable to build a valid expression. The RPN stack should have just one item.')

        return stack.pop()

    def _find_matcher(self, alias):
        """ Finds a matcher based on the given alias or raises an error if no
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

    def _init_matcher(self, *args, **kwargs):
        """ Executes the current matcher appending it to the expression """
        matcher = self.matcher(*args, **kwargs)
        self.expr.append(matcher)
        self.matcher = None
        return matcher

    def described_as(self, description, *args):
        """ Specify a custom message for the matcher """
        self.description = description.format(*args)
        return self

    def desc(self, description, *args):
        """ Just an alias to described_as """
        return self.described_as(description, *args)

    def __getattr__(self, name):
        """ Overload property access to interpret them as matchers. """

        # Ignore private (protocol) methods
        if name[0:2] == '__':
            raise AttributeError

        # If we still have an uninitialized matcher init it now
        if self.matcher:
            self._init_matcher()
            # In deferred mode we will resolve in the __ror__ overload
            if not self.deferred:
                self.resolve(self.value)

        # Normalize the name to split by underscore
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        parts = name.lower().split('_')
        # Check if we have a coordinator as first item
        if parts[0] == 'and':
            self.expr.append(OPERATOR.AND)
            parts.pop(0)
        elif parts[0] == 'or':
            self.expr.append(OPERATOR.OR)
            parts.pop(0)
        elif parts[0] == 'but':
            self.expr.append(OPERATOR.BUT)
            parts.pop(0)
        # If no coordinator is given assume a default one
        elif len(self.expr):
            self.expr.append(self.def_op)

        # Negation can come just after a combinator (ie: .and_not_be_equal)
        if 'not' in parts:
            self.expr.append(OPERATOR.NOT)
            parts.pop(parts.index('not'))

        if len(parts):
            name = '_'.join(parts)
        else:
            name = self.last_matcher or self.def_matcher

        self.matcher = self._find_matcher(name)
        self.last_matcher = name

        return self

    def __call__(self, *args, **kwargs):
        """ Execute the matcher just registered by __getattr__ passing any given
            arguments. If we're in deferred mode we don't resolve the matcher yet,
            it'll be done in the __ror__ overload.
        """
        if not self.matcher:
            raise TypeError('No matchers set. Usage: <value> | should.<matcher>(<expectation>)')

        self._init_matcher(*args, **kwargs)

        # In deferred mode we will resolve in the __ror__ overload
        if not self.deferred:
            self.resolve(self.value)

        return self

    def __enter__(self):
        clone = self.clone()
        self._contexts.append(clone)
        self.reset()
        return self

    def __exit__(self, exc, value, trace):
        # If an assertion failed inside the block just raise that one
        if isinstance(value, AssertionError):
            return False

        expr = self._contexts.pop()
        result = ContextManagerResult(exc, value, trace)
        expr.resolve(result)
        return True


class ExpectationNot(Expectation):
    """ Negates the result of the matcher """

    def _assertion(self, matcher, value):
        hc.assert_that(value, IsNot(matcher))


class ExpectationAny(Expectation):
    """ Succeeds if any of the items in an iterable value passes the matcher """

    def _assertion(self, matcher, value):
        hc.assert_that(value, hc.has_item(matcher))


class ExpectationAll(Expectation):
    """ Succeeds if all of the items in an iterable value pass the matcher """

    def _assertion(self, matcher, value):
        hc.assert_that(value, hc.only_contains(matcher))


class ExpectationNone(Expectation):
    """ Succeeds if none of the items in an iterable value passes the matcher """

    def _assertion(self, matcher, value):
        hc.assert_that(value, IsNot(hc.has_item(matcher)))
