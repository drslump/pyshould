"""
Patches mockito's param matcher to allow pyshould expectations.

    verify(Cls).method(should.be_truthy, should.be_less_than(10))

"""

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"

try:
    import mockito
    from pyshould.expectation import Expectation

    original = mockito.invocation.MatchingInvocation.compare

    @staticmethod
    def pyshould_compare(matcher, value):
        if isinstance(matcher, Expectation):
            try:
                expectation = matcher.clone()
                expectation.resolve(value)
                return True
            except AssertionError:
                return False
        return original(matcher, value)

    mockito.invocation.MatchingInvocation.compare = pyshould_compare

except ImportError:
    pass
