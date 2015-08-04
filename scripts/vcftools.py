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

_ANN_IDS = [
    {
        'field_name': 'ALLELE',
        'db_name': 'allele_s'
    },
    {
        'field_name': 'ANNOTATION',
        'db_name': 'annotation_s'

    },
    {
        'field_name': 'PUTATIVE_IMPACT',
        'db_name': 'putative_impact_s'

    }
{
        'field_name': 'GENE_NAME_HGNC',
        'db_name': 'gene_name_hgnc_s'

    }
{
        'field_name': 'GENE_ID',
        'db_name': 'gene_id_s'

    }
{
        'field_name': 'FEATURE_TYPE',
        'db_name': 'feature_type_s'

    }
{
        'field_name': 'FEATURE_ID',
        'db_name': 'feature_id_s'

    }
{
        'field_name': 'TRANSCRIPT_BIOTYPE',
        'db_name': 'transcript_biotype_s'

    }    
{
        'field_name': 'RANK_TOTAL',
        'db_name': 'rank_total_s'

    }
{
        'field_name': 'HGVS.c',
        'db_name': 'hgvs.c_s'

    }    
{
        'field_name': 'HGVS.p',
        'db_name': 'hgvs.p_s'

    }  
{
        'field_name': 'cDNA_POSITION',
        'db_name': 'cdna_position_s'

    }  
{
        'field_name': 'CDS_POSITION',
        'db_name': 'cds_position_s'

    }  
{
        'field_name': 'PROTEIN_POSITION',
        'db_name': 'protein_position_s'

    }      
{
        'field_name': 'DISTANCE_TO_FEATURE',
        'db_name': 'distance_to_feature_i'

    }      
{
        'field_name': 'ERROR_MESSAGE',
        'db_name': 'error_message_s'

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
    for record in vcf_reader:
        sys.stdout.write(json.dumps(flatten_vcf(record), sort_keys=True, indent=4, separators=(',', ': ')))
        sys.stdout.write("\n")

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
