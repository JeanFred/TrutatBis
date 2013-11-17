# -*- coding: utf-8 -*-

"""Converting the index from the Archives in a suitable format."""

__authors__ = 'User:Jean-Frédéric'

import codecs
import sys
import re
import StringIO
from collections import Counter

import pywikibot.textlib as textlib
from uploadlibrary import UnicodeCSV
from StringFunctions import *

reload(sys)
sys.setdefaultencoding('utf-8')


def identify_place_type(place_type):
    """
    Identifies the type of the given geoname.
    It first inferes the type from the metadata file, then identifies using regular expressions.
    """
    if re.search("Lieu", place_type):
        if re.search("RUE$", place_type):
            return 11
        elif re.search("AVENUE$", place_type):
            return 12
        elif re.search("ALLEE$", place_type):
            return 13
        elif re.search("ALLEES$", place_type):
            return 14
        elif re.search("PLACE$", place_type):
            return 15
        elif re.search("SQUARE$", place_type):
            return 16
        elif re.search("QUAI$", place_type):
            return 17
        elif re.search("BOULEVARD$", place_type):
            return 18
        elif re.search("QUARTIER", place_type):
            return 18
        elif re.search("PORT$", place_type):
            return 19  # Classified as Edifice, but Street for our purposes

        elif re.search("COMMUNE$", place_type):
            return 30
        elif re.search("HAMEAU$", place_type):
            return -1
        else:
            #print place_type
            return 40

    elif re.search("Edifice", place_type):
        if re.search("STATUE$", place_type):
            return -1
        if re.search("PARTICULIER$", place_type):
            return -1
        else:
            #print "Edifice drop out %s"%geoname
            return 9

    else:
        print "Cannot match geoname %s" % geoname
        return -1

def extract_from_cote(cote):
    """Return the identifiers for a given cote text."""
    groups = cote.split(' - ')
    for group in groups:
        for item in extract_from_range(group):
            yield item


def extract_from_range(text):
    """Return the identifiers for a given textual range."""
    pattern = re.compile(u"""
        51Fi               # The beginning of the ID pattern
        (?P<begin>\d+)?    # Some digits
        \sà\s              # Whitespace, 'à', whitespace
        (?P<end>\d+)?      # Some digits
        """, re.UNICODE + re.X)
    match = re.search(pattern, text)
    if match:
        for num in range(int(match.group('begin')),
                         int(match.group('end')) + 1):
            yield "51Fi{0:03d}".format(num)
    else:
        yield text


def read_csv(csv_file, delimiter):
    """Read the CSV file and return each line."""
    file_handler = codecs.open(csv_file, 'r', 'utf-8')
    return UnicodeCSV.unicode_csv_dictreader(file_handler,
                                             delimiter=delimiter)

def get_mapper(index_file):
    csvreader = read_csv(index_file, ';')
    mapper = {}
    place_type_mapper = {}
    counter = Counter()
    for row in csvreader:
        # Extracting identifier => name
        for cote in extract_from_cote(row['Cote']):
            if cote not in mapper:
                mapper[cote] = []
            mapper[cote].append(row['Nom'])
            counter[row['Nom']] += 1

        # Extracting name => level
        place_type_mapper[row['Nom']] = identify_place_type(row['Type'])
    return mapper, place_type_mapper

def main():
    """Main method."""
    mapper, place_type_mapper = get_mapper('index.csv')
    #print write_counter_values(counter)
    for key in sorted(mapper.iterkeys()):
        print "\n== %s ==" % key
        for item in mapper[key]:
            #place_type = place_type_mapper[item]
            #print item
            #if place_type >= 0 and place_type < 10:
            #    print makeCategoryFromPlace(item, "")
            #    return None
            print "[[Category:%s]]" % makeCategoryFromPlace(item, '')

def write_counter_values(counter):
    output = StringIO.StringIO()
    alignment_template = 'User:Jean-Frédéric/AlignmentRow'.encode('utf-8')
    write_counter_as_wiki(counter, output, alignment_template)
    contents = output.getvalue()
    return contents


def write_counter_as_wiki(counter, fh, template):
    """Write a given dictionary on disk, in template alignment format."""
    fh.write("""\
{| class='wikitable' border='1'
|-
! Item
! Count
! Tag
! Categories
""")
    for name, count in counter.most_common():
        values = (template,
                {'item': name, 'count': count,
                'value': "", 'categories': ""})
        table_line = ('\n' + textlib.glue_template_and_params(values))
        fh.write(unicode(table_line))
    fh.write("\n|}")

def makeCategoryFromPlace(place, city):
    """

    """
    placeR = re.search(r"(?P<place1>.+?) \((?P<place2>.+?)\)$", place)
    if placeR:
        place1 = placeR.group('place1')
        place2 = placeR.group('place2')
        if re.search(u"'$", place2):
            category = "%s%s" % (place2, place1.capitalize())
        else:
            category = "%s %s" % (place2, place1.capitalize())
    else:
        category = place.capitalize()
    category = capitalizePlace(category)
    return "%s (%s)" % (capitalizeFirst(category), city)


def makeCategoryFromCity(place):
    placeR = re.search(r"(?P<place1>.+?) \((?P<place2>.+?)\)$", place)
    if placeR:
        place1 = placeR.group('place1')
        place2 = placeR.group('place2')
        category = place1.capitalize()

    category = capitalizePlace(category)
    return capitalizeFirst(category)


if __name__ == "__main__":
    main()
