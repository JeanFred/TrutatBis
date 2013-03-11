# -*- coding: latin-1 -*-

"""Partnership with the MHNT."""

__authors__ = 'User:Jean-Frédéric'

import os
import sys
from uploadlibrary import metadata
from uploadlibrary.UploadBot import DataIngestionBot
from uploadlibrary.PostProcessing import process_DIMS
reload(sys)
sys.setdefaultencoding('utf-8')


class TrutatBisMetadataCollection(metadata.MetadataCollection):

    """Handling the metadata collection."""

    def handle_record(self, image_metadata):
        """Handle a record."""
        filename = "FRAC31555_%s.jpg" % image_metadata['Cote']
        path = os.path.abspath(os.path.join('.', 'images', filename))
        self.fields.update(image_metadata.keys())
        return metadata.MetadataRecord(path, image_metadata)


def main(args):
    """Main method."""
    collection = TrutatBisMetadataCollection()
    csv_file = 'metadata.csv'
    collection.retrieve_metadata_from_csv(csv_file, delimiter=';')

    alignment_template = 'User:Jean-Frédéric/AlignmentRow'.encode('utf-8')

    if args.make_alignment:
        for key, value in collection.count_metadata_values().items():
            collection.write_dict_as_wiki(value, key, 'wiki',
                                          alignment_template)

    if args.post_process:
        mapping_fields = ['Type de document', 'Format', 'Support', 'Technique']
        collection.retrieve_metadata_alignments(mapping_fields,
                                                alignment_template)
        mapping = {
            'Format': process_DIMS,
            }
        reader = collection.post_process_collection(mapping)
        template_name = 'User:Jean-Frédéric/TrutatBis/Ingestion'.encode('utf-8')
        titlefmt = "%(Titre)s - Fonds Trutat - %(Cote)s"
        uploadBot = DataIngestionBot(reader=reader,
                                     titlefmt=titlefmt,
                                     pagefmt=template_name)
        if args.upload:
            uploadBot.doSingle()
        elif args.dry_run:
            uploadBot.dry_run()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Process metadata and upload to Commons")
    parser.add_argument('--make-alignment', action="store_true",
                        help='')
    parser.add_argument('--post-process', action="store_true",
                        help='')
    parser.add_argument('--dry-run', action="store_true",
                        help='')
    parser.add_argument('--upload', action="store_true",
                        help='')
    arguments = parser.parse_args()
    main(arguments)
