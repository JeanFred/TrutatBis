# -*- coding: utf-8 -*-

"""Converting the index from the Archives in a suitable format."""

__authors__ = 'User:Jean-Frédéric'

import codecs
from uploadlibrary import UnicodeCSV
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


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
