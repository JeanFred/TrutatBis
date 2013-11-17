# -*- coding: latin-1 -*-

"""Partnership with the MHNT."""

__authors__ = 'User:Jean-Frédéric'

import os
import sys
from uploadlibrary import metadata
from uploadlibrary.UploadBot import DataIngestionBot, UploadBotArgumentParser
import uploadlibrary.PostProcessing as commonprocessors
import processors
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

    if args.post_process:
        mapping_fields = ['Support', 'Technique', 'Auteur', 'Places']
        mapper = commonprocessors.retrieve_metadata_alignments(mapping_fields,
                                                alignment_template)
        mapping_methods = {
            'Format': (processors.parse_format, {}),
            'Analyse': (processors.look_for_date, {}),
            'Auteur': (commonprocessors.process_with_alignment, {'mapper': mapper}),
            'Support': (commonprocessors.process_with_alignment, {'mapper': mapper}),
            'Technique': (commonprocessors.process_with_alignment, {'mapper': mapper}),
            'Cote': (processors.match_identifier_to_categories, {'mapper': mapper}),
            }
        print "Ready to post-process..."
        reader = collection.post_process_collection(mapping_methods)
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