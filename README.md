## EXPECTATIONS ##

Expectations are defined in by using a subject-predicate form that mimics
english natural language. Basically they take the form "`subject` `|` _should_.`predicate`"
where `subject` is a python expression and `predicate` defines matchers and expected
values.

Any python expressions can be used before _should_, although lambdas and other
complex expressions should be enclosed in parens to ensure a proper interpretation.

Matchers in the `predicate` part can have an expected value, this value should be
given between parens, as with a normal method call. It will be used as an argument to
the matcher function. If the matcher doesn't require an expected value there is no
need to use it as a method call.

See the following examples of expectations:

    result | should.be_integer
    (1+1) | should_not.equal(1)
    "foo" | should.be('foo')
    len([1,2,3]) | should.be_greater_than(2);
    result | should.equal(1/2 + 5)
    1 | should_not.eq(2)
    True | should.be_truthy


## COORDINATION ##

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


