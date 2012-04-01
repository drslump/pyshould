import re
from difflib import get_close_matches

import hamcrest as hc

# Words to ignore when looking up matchers
IGNORED_WORDS = ['should', 'to', 'be', 'a', 'an', 'is', 'the', 'as']

# Map of registered matchers as alias:callable
matchers = {}
# Map of normalized matcher aliases as normalized:alias
normalized = {}


def register(matcher, *aliases):
    """
    Register a matcher associated to one or more aliases. Each alias
    given is also normalized.
    """
    # For each alias given register the matcher
    for alias in aliases:
        matchers[alias] = matcher
        # Map a normalized version of the alias
        norm = normalize(alias)
        normalized[norm] = alias
        # Map a version without snake case
        norm = norm.replace('_', '')
        normalized[norm] = alias

def unregister(matcher):
    """
    Unregister a matcher (or alias) from the registry
    """

    # If it's a string handle it like an alias
    if isinstance(matcher, basestring) and matcher in matchers:
        matcher = matchers[matcher]

    # Find all aliases associated to the matcher
    aliases = [k for k, v in matchers.iteritems() if v == matcher]
    for alias in aliases:
        del matchers[alias]
        # Clean up the normalized versions
        norms = [k for k, v in normalized.iteritems() if v == alias]
        for norm in norms:
            del normalized[norm]

    return len(aliases) > 0

def normalize(alias):
    """
    Normalizes an alias by removing adverbs defined in IGNORED_WORDS
    """

    # Convert from CamelCase to snake_case
    alias = re.sub(r'([a-z])([A-Z])', r'\1_\2', alias)
    # Ignore words
    words = alias.lower().split('_')
    words = filter(lambda(x): x not in IGNORED_WORDS, words)
    return '_'.join(words)

def lookup(alias):
    """
    Tries to find a matcher callable associated to the given alias. If
    an exact match does not exists it will try normalizing it and even
    removing underscores to find one.
    """

    if alias in matchers:
        return matchers[alias]
    else:
        norm = normalize(alias)
        if norm in normalized:
            alias = normalized[norm]
            return matchers[alias]

    # Check without snake case
    if -1 != alias.find('_'):
        norm = normalize(alias).replace('_', '')
        return lookup(norm)

    return None

def suggest(alias, max=3, cutoff=0.5):
    """
    Suggest a list of aliases which are similar enough
    """

    list = matchers.keys()
    similar = get_close_matches(alias, list, n=max, cutoff=cutoff)

    return similar


# Matchers should be defined with verbose aliases to allow the use of
# natural english where possible. When looking up a matcher common adverbs
# like 'to', 'be' or 'is' are ignored in the comparison.

register(hc.equal_to,
    'be_equal_to', 'be_eql_to', 'be_eq_to')
register(hc.instance_of,
    'be_an_instance_of', 'be_a', 'be_an')
register(hc.same_instance,
    'be_the_same_instance_as', 'be_the_same_as', 'be')

register(hc.has_entry,
    'have_the_entry', 'contain_the_entry')
register(hc.has_entries,
    'have_the_entries', 'contain_the_entries')
register(hc.has_key,
    'have_the_key', 'contain_the_key')
register(hc.has_value,
    'have_the_value', 'contain_the_value')
register(hc.is_in,
    'be_in')
register(hc.has_item,
    'have_the_item', 'contain_the_item')
register(hc.has_items,
    'have_the_items', 'contain_the_items')
register(hc.contains_inanyorder,
    'have_in_any_order', 'contain_in_any_order')
register(hc.contains,
    'have', 'contain')
register(hc.only_contains,
    'have_only', 'contain_only')
register(hc.close_to,
    'be_close_to')
register(hc.greater_than,
    'be_greater_than', 'be_gt')
register(hc.greater_than_or_equal_to,
    'be_greater_than_or_equal_to', 'be_ge')
register(hc.less_than,
    'be_less_than', 'be_lt')
register(hc.less_than_or_equal_to,
    'be_less_than_or_equal_to', 'be_le')
register(hc.has_length,
    'have_length')
register(hc.has_property,
    'have_the_property', 'contain_the_property')
register(hc.has_string,
    'have_the_string', 'contain_the_string')
register(hc.equal_to_ignoring_case,
    'be_equal_to_ignoring_case')
register(hc.equal_to_ignoring_whitespace,
    'be_equal_to_ignoring_whitespace')
#register(hc.contains_string, 'have_the_string', 'contain_the_string')
register(hc.ends_with,
    'end_with')
register(hc.starts_with,
    'start_with', 'begin_with')


