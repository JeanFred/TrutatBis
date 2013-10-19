# -*- coding: utf-8 -*-

"""Unit tests for index_converter."""

import unittest
from index_converter import extract_from_range, extract_from_cote


class TestIndexConverter(unittest.TestCase):

    """Unit tests for index_converter."""

    def test_extract_from_range(self):
        """Test extract_from_range()."""
        values = [
            (u'51Fi353 à 356', ['51Fi353', '51Fi354', '51Fi355', '51Fi356']),
            (u'51Fi242 à 244', ['51Fi242', '51Fi243', '51Fi244']),
            (u'51Fi425', ['51Fi425']),
            ]
        for value, expected in values:
            result = list(extract_from_range(value))
            self.assertEqual(result, expected)

    def test_extract_from_cote(self):
        """Test extract_from_cote()."""
        values = [
            (u'51Fi353 à 356 - 51Fi395 - 51Fi461 à 462',
             ['51Fi353', '51Fi354', '51Fi355', '51Fi356', u'51Fi395', '51Fi461', '51Fi462']),
            (u'51Fi425', ['51Fi425']),
            ]
        for value, expected in values:
            result = list(extract_from_cote(value))
            self.assertEqual(result, expected)
