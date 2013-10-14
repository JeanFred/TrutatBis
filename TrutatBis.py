# -*- coding: latin-1 -*-

"""Partnership with the MHNT."""

__authors__ = 'User:Jean-Frédéric'

import os
import sys
from uploadlibrary import metadata
from uploadlibrary.UploadBot import DataIngestionBot, UploadBotArgumentParser
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
        front_titlefmt = ""
        variable_titlefmt = "%(Titre)s"
        rear_titlefmt= " - Fonds Trutat - %(Cote)s"
        uploadBot = DataIngestionBot(reader=iter(collection.records),
                                     front_titlefmt=front_titlefmt,
                                     rear_titlefmt=rear_titlefmt,
                                     variable_titlefmt=variable_titlefmt,
                                     pagefmt=template_name)
        if args.upload:
            uploadBot.doSingle()
        elif args.dry_run:
            uploadBot.dry_run()


if __name__ == "__main__":
    parser = UploadBotArgumentParser()
    arguments = parser.parse_args()
    if not any(arguments.__dict__.values()):
        parser.print_help()
    else:
        main(arguments)