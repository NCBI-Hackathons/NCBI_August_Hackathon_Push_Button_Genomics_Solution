import logging
import pysam

from multiprocessing import Process
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from browser.models import Gene

logger = logging.getLogger('browser.management')


class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.gff_file = None
        self.num_threads = 1
        self.features = ['gene', 'transcript', 'exon']
        self.tabix_reader = None

    args = '<gff_file>'
    help = 'Load genes annotation from GFF file'
    option_list = BaseCommand.option_list + (
        make_option('-t', '--threads',
                    action='store',
                    type='int',
                    dest='threads',
                    default=1,
                    help='Number of threads to use [default: 1].'),
        make_option('-a', '--feature',
                    action='append',
                    type='string',
                    dest='features',
                    default=[],
                    help='Feature types to import, can be provided multiple times'
                         ' [default: gene, transcript and exon].'),
        )

    def helper(self, thread=0):
        for contig in self.tabix_reader.contigs[thread::self.num_threads]:
            load_genes_helper(self.tabix_reader.fetch(contig, start=0, parser=pysam.asGTF(), multiple_iterators=True),
                              features=self.features)

    def handle(self, *args, **options):
        try:
            self.gff_file = args[0]
        except IndexError:
            raise CommandError('Please provide a GFF file.')

        self.num_threads = options['threads']
        if options['features']:
            self.features = options['features']

        try:
            self.tabix_reader = pysam.Tabixfile(self.gff_file)
        except IOError as e:
            raise CommandError("Error opening '{gff_file}': {error}".format(gff_file=self.gff_file, error=e))

        # drop all existing data
        Gene.objects.all().delete()

        if self.num_threads > 1:
            for i in range(self.num_threads):
                p = Process(target=self.helper, kwargs={'thread': i})
                p.start()
        else:
            self.helper()

        logger.info("Successfully imported GFF file: '{gff_file}'.".format(gff_file=self.gff_file))


def set_extra_attrs(feature, attrs):
    """
    Sets any extra attribute a feature might have.

    :param feature: feature
    :param attrs: attributes to add
    """
    for attr in attrs:
        if not hasattr(feature, attr):
            setattr(feature, attr, attrs[attr])


def load_genes_helper(tabix_reader, features=None):
    """
    Helper for load genes command.

    Loads genes annotation in GFF format.

    :param tabix_reader: Tabix Reader.
    """
    if features is None:
        features = ['gene', 'transcript', 'exon']

    # iterate over every record
    for record in tabix_reader:
        # skip line if record feature not in features
        if record.feature not in features:
            continue

        attrs = dict()
        for attr in record.attributes.split(';'):
            if attr != '':
                key, value = attr.strip().split('=', 1)
                attrs[key] = value.strip('"')

        # parse dbxref
        db_xref = {}
        for xref in attrs['Dbxref'].split(','):
            db, d_id = xref.split(':')[-2:]
            db_xref[db] = d_id

        # skip if didn't get our primary database id
        if 'GeneID' not in db_xref:
            continue

        # create gene entry
        feature = Gene(
            slug=db_xref['GeneID'],
            gene_name_upper=attrs['gene'].upper(),
            gene_name=attrs['gene'],
        )

        # grab common attributes
        feature.chrom = record.contig
        feature.strand = record.strand
        feature.start = record.start
        feature.end = record.end

        # finally save the feature to the database
        try:
            feature.save()
        except ValidationError as e:
            logger.warning("Skipping. Failed to import feature. Error: {error}".format(error=e))
            logger.warning("Corrupted record: {record}".format(record=record))
            continue
        except IntegrityError as e:
            logger.warning("Skipping import of '{feature}': {error}".format(feature=feature.slug, error=e))
