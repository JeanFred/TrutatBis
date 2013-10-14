# -*- coding: latin-1 -*-

"""Parsers useful for Archives metadata."""

__authors__ = 'User:Jean-Frédéric'

import re


def parse_format(field, old_field_value):
    """Parse a foramt and return the parsed."""
    new_value = parse_format_unwrapped(old_field_value)
    return {field: new_value}


def _clean_dim(dim):
    """Clean a dimension-like string"""
    return re.sub(r"\s?,\s?", '.', dim).strip()


def parse_format_unwrapped(text):

    def repl(m):
        """Convert the pattern matchd in {{Size}}."""
        unit = 'cm'
        elements = m.groupdict()
        l = filter(None, [elements[x] for x in sorted(elements.keys())])
        s = '|'.join([_clean_dim(dim) for dim in l])
        return " {{Size|%s|%s}}" % (unit, s)

    format_pattern = re.compile(r"""
        (?P<a>[\d,\.]+?)   # Digits, comma or dot, captured as group
        \s*x\s*            # Whitespace, x, whitespace
        (?P<b>[\d,\.]+?)   # Same
        \s*$               # Whitespace until the end
        """, re.X)

    new_value = re.sub(format_pattern, repl, text)
    return new_value

