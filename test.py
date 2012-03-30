from pyshould import *


'a' | should.equal_to('a')
1 | should.be_less_than(10)

it(1).should_be_less_than(10)
any([10,3]).should_be_less_than(10)
any_of([10,3]).should_be_less_than(10)
all([3,3]).should_be_less_than(10)
all_of([3,3]).should_be_less_than(10)
none([11,13]).should_be_less_than(10)
none_of([11,13]).should_be_less_than(10)

[3,3] | should_all.be_less_than(10)

1 | should_not.be_equal_to(2)



