import json
import logging
import sys
import vcf

from mando import command, main

logger = logging.getLogger('vcf_to_json')

_IDS = [
    {
        'field_name': 'CHROM',
        'db_name': 'chrom_s'
    },
    {
        'field_name': 'REF',
        'db_name': 'ref_s'
    },
    {
        'field_name': 'QUAL',
        'db_name': 'qual_s'
    },
    {
        'field_name': 'POS',
        'db_name': 'pos_s'
    },
    {
        'field_name': 'ALT',
        'db_name': 'alt_ss'
    },
    {
        'field_name': 'FILTER',
        'db_name': 'filter_s'
    },
    {
        'field_name': 'FORMAT',
        'db_name': 'format_s'
    },
    {
        'field_name': 'ID',
        'db_name': 'id_s'
    }
]

_INFO_IDS = [
    {
        'field_name': 'SNPEFF_GENE_NAME',
        'db_name': 'gene_name_s'
    },
    {
        'field_name': 'SNPEFF_IMPACT',
        'db_name': 'impact_s'

    },
    {
        'field_name': 'SNPEFF_CODON_CHANGE',
        'db_name': 'codon_change_i'

    }

]

@command('vcf-to-json')
def vcf_to_json(vcf_file):
    """
    VCF to json converter.

    :param vcf_file: VCF file.
    """
    vcf_reader = vcf.Reader(filename=vcf_file)

    # iterate over every record
    sys.stdout.write("[\n")
    for record in vcf_reader:
        sys.stdout.write(json.dumps(flatten_vcf(record), sort_keys=True, indent=4, separators=(',', ': ')))
        sys.stdout.write("\n")
    sys.stdout.write("]\n")


def flatten_vcf(record):
    """
    :param VCFRecord record: VCFRecord object
    :return dict: all fields as a flat dictionary, including those fields in rec.INFO
    """

    # gather field values
    d = {}
    for _id in _IDS:
        field_name = _id['field_name']
        db_name = _id['db_name']

        # make sure to deal with any special case
        if field_name == 'ALT':
            field = [str(a) for a in getattr(record, field_name) if a is not None]
        else:
            field = getattr(record, field_name)

        # skip null values
        if field is None:
            continue

        d[db_name] = field

    for _id in _INFO_IDS:
        field_name = _id['field_name']
        db_name = _id['db_name']

        if field_name in record.INFO and record.INFO[field_name] is not None:
            d[db_name] = record.INFO[field_name]

    return d

def flatten_list(l):
    return l[0] if type(l) == list else l

def name_field(field, value=None):
    if value is None:
        return field

if __name__ == "__main__":
    main()
