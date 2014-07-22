__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"

import os


class Dumper(object):
    """ Dumps a value when the equality comparison is triggered
    """

    UNSET_VALUE = {}
    REPORTER = lambda x: os.sys.stdout.write(x + os.linesep)

    def __init__(self, value=UNSET_VALUE, msg=None, reporter=REPORTER):
        self.value = value
        self.msg = msg
        self.reporter = reporter

    def __call__(self, value=UNSET_VALUE, msg=None, reporter=None):
        """ Generate a new dumper based on the configuration 
        """
        return Dumper(value=value, msg=msg, reporter=reporter or self.reporter)

    def __eq__(self, other):
        if self.msg != None:
            self.reporter(self.msg + ': ' + repr(other))
        else:
            self.reporter(repr(other))

        if self.value is not Dumper.UNSET_VALUE:
            return self.value == other

        return True

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.value is Dumper.UNSET_VALUE:
            return '<dumper>'
        return repr(self.value)
