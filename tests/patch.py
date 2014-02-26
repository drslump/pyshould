try:
    import unittest2 as unittest  # Python 2.6
except:
    import unittest

import pyshould.patch


class PatchTestCase(unittest.TestCase):
    """ Simple tests for the patched object api """

    def setUp(self):
        import platform
        is_cpython = (
            hasattr(platform, 'python_implementation')
            and platform.python_implementation().lower() == 'cpython')

        if not is_cpython:
            raise unittest.SkipTest('patch is only available under cpython, skipping test')

    def test_should(self):
        from pyshould.expectation import Expectation
        assert isinstance(self.should, Expectation)
        self.should.be_a(unittest.TestCase)

    def test_should_apply(self):
        import json
        '{"foo":"bar"}'.should(json.loads).have_key('foo')

    def test_should_int(self):
        (1).should.eq(1)
        (3).should.not_eq(2)

    def test_should_str(self):
        'foo'.should.eq('foo')
        'foo'.should.not_eq('bar')

    def test_should_none(self):
        None.should.be_none()

    def test_should_not(self):
        (1).should_not.eq(2)

    def test_should_not_none(self):
        None.should_not.eq(2)

    def test_should_all(self):
        [1,2,3].should_all.be_int()

    def test_should_any(self):
        [1,2,3].should_any.eq(2)

    def test_should_none(self):
        [1,2,3].should_none.eq(5)

    def test_should_all_none(self):
        try:
            None.should_all.be_int()
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass

    def test_should_fail(self):
        try:
            'foo'.should.eq('bar')
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass

    def test_should_fail_none(self):
        try:
            None.should.eq('bar')
            raise RuntimeError('We should not reach this point')
        except AssertionError:
            pass
