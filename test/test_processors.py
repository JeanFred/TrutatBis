# -*- coding: utf-8 -*-

import unittest
from processors import parse_format_unwrapped, look_for_date_unwrapped


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

    def test_look_for_date(self):
        values = [
            ("Gare Matabiau, quai et voie. 4 octobre 1899. Vue d'ensemble",
             ('1899-10-04', '1899')),  # FullDateR

            ("Café Albrighi. Juillet 1905. Vue du café prise",
             ('1905-07', '1905')),  # MonthDateR

            ("Place des Carmes, côté nord. Vers 1905. Vue ",
             ('{{Other date|circa|1905}}', '1905')),  # circaYearR

            ("Place des Carmes, côté nord. Vers juillet 1905.Vue perspective",
             ('{{Other date|circa|1905-07}}', '1905')),  # circaDateR

            ("toulousaine. Entre 1888 et 1907. Vue de face d'une automobile",
             ('{{Other date|between|1888|1907}}', None)),  # betweenDateR

            (u"Entre les années 1859 et 1907. Vue d'une nature morte",
             ('{{Other date|between|1859|1907}}', None)),  # betweenDateR bis

            ("Joseph Delmas en costume d’Adam. Atelier Vidal. 1861 ou 1862",
             ('{{Other date|or|1861|1862}}', None)),  # orDateR

            (u"Jules-Guesde. Années 1890. Vue d'ensemble en",
             ('{{Other date|decade|1890}}', None)),  # decadeDateR

            (u"maritime escarpée. 19e siècle. Vue d'ensemble",
             ('{{Other date|century|19}}', None)),  # centuryR

            (u"Carcassonne (Aude). Fin 19e siècle. Vue d'ensemble",
             ("{{Other date|end|{{Other date|century|19}}}}", None)),  # centuryR bis

            ("Villeneuve les Avignon. Tour de Philippe le Bel. 1897",
             (None, None)),  # Regular year - nothing
        ]

        for value, expected in values:
            self.assertEqual(look_for_date_unwrapped(value), expected)
