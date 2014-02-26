"""
Prints the configured matchers when run with `python -m pyshould`
"""

def main():
    from pyshould.matchers import lookup, aliases, alias_help
    group = {}
    for alias in aliases():
        m = lookup(alias)
        if m not in group:
            group[m] = []
        group[m].append(alias)

    for items in group.values():
        print("{0}:\n\t{1}\n".format(
            ', '.join(items),
            alias_help(items[0]).replace("\n", "\n\t")
        ))


main()
