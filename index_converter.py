# -*- coding: utf-8 -*-

"""Converting the index from the Archives in a suitable format."""

__authors__ = 'User:Jean-Frédéric'

import codecs
from uploadlibrary import UnicodeCSV
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


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


def main():
    """Main method."""
    csvreader = read_csv('index.csv', ';')
    mapper = {}
    for row in csvreader:
        print row


if __name__ == "__main__":
    main()
