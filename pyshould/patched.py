from hamcrest.core.core.isnot import IsNot as orig_IsNot

class IsNot(orig_IsNot):
    """
    Extends the IsNot matcher to improve its mismatch message
    """

    def describe_mismatch(self, item, desc):
        if getattr(self.matcher, 'describe_mismatch', None):
            self.matcher.describe_mismatch(item, desc)
        else:
            orig_IsNot.describe_mismatch(self, item, desc)

