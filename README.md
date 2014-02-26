PyShould
========

[![Version](https://pypip.in/v/pyshould/badge.png)](https://crate.io/packages/pyshould)
[![Downloads](https://pypip.in/d/pyshould/badge.png)](https://crate.io/packages/pyshould)
[![Build Status](https://travis-ci.org/drslump/pyshould.png)](https://travis-ci.org/drslump/pyshould)

**PyShould** is a Python DSL allowing to write expectations or assertions in 
_almost_ natural language. The goal is to offer an expressive yet readable syntax
to define the expectations in detail. 

Under the hood it uses the [PyHamcrest](http://packages.python.org/PyHamcrest/) 
library of matchers to **build complex matching predicates with ease** and offer 
**great explanations** when there is a mismatch.

Its primary use case is in unit testing, replacing the need for Python's native
`assertX` methods. Its use is completely transparent to the unit testing runner
used, since mismatches are reported using the standard `AssertionError`.


## Installation and basic usage

If you don't want to mess with the code the easier way to install is with `pip`:

    pip install pyshould

The installation procedure is based on _setuptools_ so it's pretty simple to get 
going. In order to install from a checkout of the repository you can just issue the
following command:

    python setup.py install

Now you'll be able to access **PyShould** by importing the package `pyshould`. It's
designed to be used with a _wildcard import_ although if you prefer you can just 
import those DSL keywords you need. Here are some examples on different ways to import
the library in your code:

```python
from pyshould import *
from pyshould import should
from pyshould import should, should_not, all_of
```


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

> **TIP** Run the following to print all the configured expectations with
a description of what they do: `python -m pyshould` (use `python -m pyshould.__main__`
for Python 2.6)

See the following examples of expectations:

```python
from pyshould import *

result | should.be_integer()
(1+1) | should_not.equal(1)
"foo" | should.equal('foo')
len([1,2,3]) | should.be_greater_than(2);
result | should.equal(1/2 + 5)
1 | should_not.eq(2)
# Matchers not requiring a param can skip the call parens
True | should.be_truthy

# Check for exceptions with the context manager interface
with should.throw(TypeError):
    raise TypeError('foo')

with should.not_raise:  # will report a failure
    fp = open('does-not-exists.txt')

# Apply our custom logic for a test
'FooBarBaz' | should.pass_callback(lambda x: x[3:6] == 'Bar')
```


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

```python
should.be_an_integer.or_string.and_equal(1)
# (integer) OR (string AND equal 1)

should.be_an_integer.or_a_float.or_a_string
# (integer) OR (float) OR (string)
should.be_an_integer.or_a_string.and_equal_to(10).or_a_float
# (integer) OR (string AND equal 10) OR (float)

should.be_an_integer.or_a_string.but_less_than(10)
# (integer OR string) AND (less than 10)

# Note: we can use spacing to make them easier to read
should.be_an_integer  .or_a_string.and_equal(0)  .or_a_float
# (integer) OR (string AND equal 0) OR (float)

# Note: in this case we use capitalization to make them more obvious
should.be_an_integer .Or_a_string.And_equal(1) .But_Not_be_a_float
# ( (integer) OR (string AND equal 1) ) AND (not float)

# Note: if no matchers are given the last one is used
should.be_equal_to(10).Or(20).Or(30)
# (equal 10) OR (equal 20) OR (equal 30)

# Note: If no combinator is given AND is used by default
should.integer.greater_than(10).less_than(20)
# (integer) AND (greater than 10) AND (less than 20)

# Note: But by using should_either we can set OR as default
should_either.equal(10).equal(20).equal(30)
# (equal 10) OR (equal 20) OR (equal 30)
```


## Quantifiers

Using the standard syntax it's possible to define a matcher in conjunction
with a quantifier. These are specially useful when working with iterable
values.

```python
[1, 2] | should_all.be_int
(1, 2) | should_any.equal(1)
iterable | should_none.be_empty
```

We can also define directly a matcher without using the pipe syntax by
wrapping the value to test in a quantifier keyword.

```python
it(1).should_equal(1)
it(0).to_equal(0)
any_of(1, 3).to_equal(1)
all_of([1, 3]).should_be_int()
none_of(1, 3).to_eq(0)
```


## Alternative syntax

Besides the standard syntax shown above (aka _pipe syntax_) it's also possible
to use other syntaxes by using the `expect` module, although it doesn't support
coordinated expressions (use of and, or, but).

```python
from pyshould.expect import expect, expect_all, expect_any, expect_none

expect(1).to_equal(1)
# Note that matchers without params need the call parens when using this syntax
expect_all(1, 3).to_be_int()
expect_any([1, 3]).to_equal(1)
expect(any_of(1,3)).to_equal(1)
```


### Patching the root object

> **NOTE** This is only supported when running under cpython.

Thanks to the great folks @clarete and @gabrielfalcao from 
[sure](https://github.com/gabrielfalcao/sure) it's possible to patch the root
object to expose special properties for testing any value. To enable this
feature you must import the `pyshould.patch` module.

> **WARNING** Once the `patch` module is imported it will *monkey patch* the
root object from which all variables are extended from in your Python
runtime. This means that every object will be extended with the following
properties: `should`, `should_not`, `should_all`, `should_any` and `should_none`.

    import pyshould.patch

    'foo'.should.eq('foo')
    data = {'foo': 'bar'}
    data.should_not.have_key('lorem')
    data.keys().should_all.be_string()


## Integration with third parties

Broadly speaking, *pyshould* expressions overload Python's equality operator, so
it's possible to use them with almost any third party library. Here is an example
of the integration with the standard unittest assertion library.

    m = should.be_an_int.and_greater_than(3)
    self.assertEqual(2, m)
    # AssertionError: 2 != (an integer and a value greater than <3>)

Michael Foord's [Mock](http://www.voidspace.org.uk/python/mock/), which is available
under `unittest.mock` from Python 3.3, will also work out of the box:

    mock(10, 1)
    mock.assert_called_with(should.any, should.be_greater_than(3))
    # AssertionError: Expected call: mock(ANYTHING, a value greater than <3>)

[Mockito](https://code.google.com/p/mockito-python/) has also been tested and works
out of the box:

    verify(MyClass).my_method(should.be_truthy, should.eq(10))


## Transforming values

An useful feature when integrating the expectations with a mocking library is to be
able to transform a value before asserting it. This can be triggered by passing a
callable as only argument to a non initialized expression (ie: `should(callable)`).

For instance you've mocked a call that will receive a Json serialized string but you
want to test if it contains a given key. Check the following example:

    mock('{"username": "drslump", "password": "foobar"}')
    mock.assert_called_with( should(json.loads).have_key('username') )

If you need to use the same transform often you could also create an expectation for
it:

    should_json = should(json.loads)
    mock.assert_called_with( should_json.have_key('username') )
    d | should_json.have_key('username')


## Custom expectations

Creating your custom expectations is fairly easy, have a look at the `matchers.py`
file for a set of examples. Basically expectations are just a thin layer of 
syntax sugar over Hamcrest's matchers, so the most difficult part is to implement
the actual matcher.

Alternatively, for those cases where we just want to test something complicated
but not create a reusable matcher, it's possible to use the `callback` expectation:

    def my_complex_assert(value):
      # NOTE: we can also return an expectation instead of a bool
      # ie: return value | should.eq(10).Or(20).but_be_greater_than(100)
      resp = request.get('http://foo.com/bar', {'q': value})
      return resp.status_code == 200

    self.foo | should.pass_callback(my_complex_assert)


## Miscellanea

I find it extremely convenient to include `should` as a keyword under my editor 
highlighting. This simple change makes the tests much more obvious and easier to 
read. Here is an example syntax for Sublime Text, just place it in a file under 
your user package directory.

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
      <key>comment</key>
      <string>Customizations to the Python syntax</string>
      <key>name</key>
      <string>Python (Customized)</string>
      <key>scopeName</key>
      <string>source.custom.python</string>
      <key>fileTypes</key>
      <array>
        <string>py</string>
      </array>
      <key>patterns</key>
      <array>
        <dict>
          <key>match</key>
          <string>\|\s*should(_(any|all|none|not|either))?\.</string>
          <key>name</key>
          <string>keyword.custom.python</string>
        </dict>
        <dict>
          <key>include</key>
          <string>source.python</string>
        </dict>
      </array>
    </dict>
    </plist>


## License

    The MIT License

    Copyright (c) 2012, 2013 Iván -DrSlump- Montes

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

