"""
Overrides for external libraries
"""
from hamcrest.core.core.isnot import IsNot as hc_IsNot

__author__  = "Ivan -DrSlump- Montes"
__email__   = "drslump@pollinimini.net"
__license__ = "MIT"


class IsNot(hc_IsNot):
    """ Extends the IsNot matcher to improve its mismatch message """

    def describe_mismatch(self, item, desc):
        if getattr(self.matcher, 'describe_mismatch', None):
            self.matcher.describe_mismatch(item, desc)
        else:
            hc_IsNot.describe_mismatch(self, item, desc)

