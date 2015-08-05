import json
import logging
import requests
import sys
import vcf

from mando import command, main

logger = logging.getLogger('vcf_to_json')

IMPACTS = {
    'LOW': 0,
    'MODIFIER': 1,
    'MODERATE': 2,
    'HIGH': 3
}

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
        'db_name': 'qual_f'
    },
    {
        'field_name': 'POS',
        'db_name': 'pos_i'
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
        'field_name': 'RS',
        'db_name': 'rs_i'
    },
    {
        'field_name': 'dbSNPBuildID',
        'db_name': 'dbsnp_build_id_i'
    },
    {
        'field_name': 'CLNSIG',
        'db_name': 'clin_sig_i'
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

    },
    {
        'field_name': 'GENE_NAME_HGNC',
        'db_name': 'gene_name_hgnc_s'

    },
    {
        'field_name': 'GENE_ID',
        'db_name': 'gene_id_s'

    },
    {
        'field_name': 'FEATURE_TYPE',
        'db_name': 'feature_type_s'

    },
    {
        'field_name': 'FEATURE_ID',
        'db_name': 'feature_id_s'

    },
    {
        'field_name': 'TRANSCRIPT_BIOTYPE',
        'db_name': 'transcript_biotype_s'

    },
    {
        'field_name': 'RANK_TOTAL',
        'db_name': 'rank_total_s'

    },
    {
        'field_name': 'HGVS.c',
        'db_name': 'hgvs.c_s'

    },
    {
        'field_name': 'HGVS.p',
        'db_name': 'hgvs.p_s'

    },
    {
        'field_name': 'cDNA_POSITION',
        'db_name': 'cdna_position_s'

    },
    {
        'field_name': 'CDS_POSITION',
        'db_name': 'cds_position_s'

    },
    {
        'field_name': 'PROTEIN_POSITION',
        'db_name': 'protein_position_s'

    },
    {
        'field_name': 'DISTANCE_TO_FEATURE',
        'db_name': 'distance_to_feature_i'

    },
    {
        'field_name': 'ERROR_MESSAGE',
        'db_name': 'error_message_s'

    },
]

@command('vcf-to-json')
def vcf_to_json(vcf_file, upload_hash=None):
    """
    VCF to json converter.

    :param vcf_file: VCF file.
    :param upload_hash: hash identifying the upload.
    """

    vcf_reader = vcf.Reader(filename=vcf_file)

    # iterate over every record
    sys.stdout.write("[\n")

    record = vcf_reader.next()
    while record:
        sys.stdout.write(
            json.dumps(flatten_vcf(record, upload_hash=upload_hash), sort_keys=True, indent=4, separators=(',', ': '))
        )
        try:
            record = vcf_reader.next()
        except StopIteration:
            break
        sys.stdout.write(",\n")

    sys.stdout.write("]\n")


def flatten_vcf(record, upload_hash=None):
    """
    :param VCFRecord record: VCFRecord object
    :param upload_hash: hash identifying the upload.
    :return dict: all fields as a flat dictionary, including those fields in rec.INFO
    """
    # create variant id
    v_id = '{chrom}-{pos}'.format(chrom=record.CHROM, pos=record.POS)

    d = {'id': v_id}

    # add upload hash
    if upload_hash is not None:
        d['upload_hash_s'] = upload_hash
        d['id'] += '--{hash}'.format(hash=upload_hash)

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

    # grab snpEff annotations
    annotations = record.INFO['ANN']
    for ann in annotations:
        # split piped annotation's fields
        fields = ann.split('|')

        d_ann = {}
        for i, _id in enumerate(_ANN_IDS):
            db_name = _id['db_name']

            # grab field value
            field = fields[i]
            if field != '':
                d_ann[db_name] = field

        # only update the annotations if it is a higher impact
        if 'putative_impact_s' not in d or IMPACTS[d['putative_impact_s']] < IMPACTS[d_ann['putative_impact_s']]:
            d.update(d_ann)

    # grab extra info fields
    for _id in _INFO_IDS:
        field_name = _id['field_name']
        db_name = _id['db_name']

        if field_name in record.INFO:
            d[db_name] = record.INFO[field_name]

    return d

if __name__ == "__main__":
    main()
