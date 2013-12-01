"""
Patches mockito's param matcher to allow pyshould expectations.

NOTE: This module has been deprecated, should expectations can
      now directly work with third party libraries by the
      overloading of the equality operators.
"""

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"

from warnings import warn

warn("patch_mockito is no longer needed", DeprecationWarning)
