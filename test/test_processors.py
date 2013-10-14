import unittest
from processors import parse_format_unwrapped


class TestProcessors(unittest.TestCase):

    def test_parse_format(self):
        values = [
            ('8,5 x 10', ' {{Size|cm|8.5|10}}'),
            ('13 x 18', ' {{Size|cm|13|18}}'),
            ('4,5 x 5,5', ' {{Size|cm|4.5|5.5}}'),
            ('7 x 9,5', ' {{Size|cm|7|9.5}}'),
        ]
        for value, expected in values:
            self.assertEqual(parse_format_unwrapped(value), expected)
