PyShould
========

**PyShould** is a Python DSL allowing to write expectations or assertions in 
_almost_ natural language. The goal is to offer an expressive yet readable syntax
to define the expectations in detail. 

Under the hood it uses the [PyHamcrest](http://packages.python.org/PyHamcrest/) 
library of matchers to build complex matching predicates and offer great
explanations when there is a mismatch.

Its primary use case is in unit testing, replacing the need for Python's native
`assertX` methods. Its use is completely transparent to the unit testing runner
used, since mismatches are reported using the standard `AssertionError`.


## Expectations

Expectations are defined in by using a subject-predicate form that mimics
english natural language. Basically they take the form:

`subject` `|` **should**.`predicate`

Where `subject` is a python expression and `predicate` defines matchers and 
expected values.

Any python expression can be used before _should_, although lambdas and other
complex expressions should be enclosed in parens to ensure a proper interpretation.

Matchers in the `predicate` part can have an expected value, this value should be
given between parens, as with a normal method call. It will be used as an argument 
to the matcher function. If the matcher doesn't require an expected value there is 
no need to use it as a method call.

See the following examples of expectations:

    from pyshould import *

    result | should.be_integer()
    (1+1) | should_not.equal(1)
    "foo" | should.be('foo')
    len([1,2,3]) | should.be_greater_than(2);
    result | should.equal(1/2 + 5)
    1 | should_not.eq(2)
    # Matchers not requiring a param can skip the call parens
    True | should.be_truthy


## Coordination

Complex expectations can be _coordinated_ by using operators `and`, `or` and
`but`. Also `not` is supported to negate the result of an expectation. It's
important to understand the operator precedence rules before using them,
although they try to follow common conventions for the english language there
might be cases where they don't quite do what they look like.

All operators are left-associative and take two operands, except for `not` which
is an unary operator, thus the precedence rules are very simple:

      operator  |  precedence index
    ---------------------------------
        not     |        4
        and     |        3
        or      |        2
        but     |        1

Expectations should be kept simple, when in doubt break up complex expectations 
into simpler ones.

Please review the following examples to see how these precedence rules
apply.

    should.be_an_integer.or_string.and_equal(1)
    (integer) OR (string AND equal 1)

    should.be_an_integer.or_a_float.or_a_string
    (integer) OR (float) OR (string)
    should.be_an_integer.or_a_string.and_equal_to(10).or_a_float
    (integer) OR (string AND equal 10) OR (float)

    should.be_an_integer.or_a_string.but_less_than(10)
    (integer OR string) AND (less than 10)

    -- Note: we can use spacing to make them easier to read
    should.be_an_integer  .or_a_string.and_equal(0)  .or_a_float
    (integer) OR (string AND equal 0) OR (float)

    -- Note: in this case we use capitalization to make them more obvious
    should.be_an_integer .Or_a_string.And_equal(1) .But_Not_be_a_float
    ( (integer) OR (string AND equal 1) ) AND (not float)

    -- Note: if no matchers are given the last one is used
    should.be_equal_to(10).Or(20).Or(30)
    (equal 10) OR (equal 20) OR (equal 30)

    -- Note: If no combinator is given AND is used by default
    should.integer.greater_than(10).less_than(20)
    (integer) AND (greater than 10) AND (less than 20)

    -- Note: But by using should_either we can set OR as default
    should_either.equal(10).equal(20).equal(30)
    (equal 10) OR (equal 20) OR (equal 30)


## Quantifiers

Using the standard syntax it's possible to define a matcher in conjunction
with a quantifier. These are specially useful when working with iterable
values.

    [1, 2] | should_all.be_int
    (1, 2) | should_any.equal(1)
    iterable | should_none.be_empty

We can also define directly a matcher without using the pipe syntax by
wrapping the value to test in a quantifier keyword.

    it(1).should_equal(1)
    it(0).to_equal(0)
    any_of(1, 3).to_equal(1)
    all_of([1, 3]).should_be_int()
    none_of(1, 3).to_eq(0)


## Alternative syntax

Besides the standard syntax shown above (aka _pipe syntax_) it's also possible
to use other syntaxes by using the `expect` module, although it doesn't support
coordinated expressions (use of and, or, but).

    from pyshould.expect import expect, expect_all, expect_any, expect_none

    expect(1).to_equal(1)
    # Note that matchers without params need the call parens when using this syntax
    expect_all(1, 3).to_be_int()
    expect_any([1, 3]).to_equal(1)
    expect(any_of(1,3)).to_equal(1)


## License

    The MIT License

    Copyright (c) 2012 Iván -DrSlump- Montes

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    'Software'), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

