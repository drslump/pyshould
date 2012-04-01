import sys
from pyshould import *
from pyshould.expect import *

1 | should_not.equal(2).or_equal(3)
#1 | should.not_equal(1).or_equal(3)

1 | should_either.equal(2).equal(3).equal(1)


1 | should.equal(2).or_equal(1).but_greaterthan(1)

expect(1).to_equal(1)
expect(1, 3).to_be_less_than(5)
expect_it(1).to_be_less_than(3)
expect_all([3,1]).to_be_less_than(5)
expect_any([3,1]).to_be_equal_to(1)
expect_none([3,1]).to_be_equal_to(5)

1 | should.equal(1).lt(10).desc('not equal or less')

20 | should.equal(20).or_less_than(10)
1 | should.equal(2).or_less_than(10)

#'a' | should.equal('a')
#1 | should.be_lessthan(10)

#it(1).should_be_less_than(10).equal(2)
#any([10,3]).should_be_less_than(10)
#all([3,3]).should_be_less_than(10)
#none([11,13]).should_be_less_than(10)

#[3,1] | should_all.be_less_than(10)

#1 | should_not.be_equal_to(2)



