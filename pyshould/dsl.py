from .should import Should, ShouldNot, ShouldAll, ShouldAny, ShouldNone

# Create instances to be used with the overloaded | operator
should = Should(deferred=True)
should_not = ShouldNot(deferred=True)
should_all = ShouldAll(deferred=True)
should_any = ShouldAny(deferred=True)
should_none = ShouldNone(deferred=True)


def it(value):
    """ Wraps a value in a should """
    return Should(value)

def any(value):
    """ At least of the items in value should match """
    return ShouldAny(value)

def all(value):
    """ All the items in value should match """
    return ShouldAll(value)

def none(value):
    """ None of the items in value should match """
    return ShouldNone(value)
