#!/bin/bash

BASE_DIR=`pwd`
#$2="test.GRCh38.dbsnp.chr22.vcf"  #placeholder for output annotated file
#python snpeff_annotator.py $BASE_DIR "/" $1 | java -jar snpEff.jar -c ./snpEff.config -v > $BASE_DIR  "/" $2
python annotation_initializer.py $BASE_DIR"/"$1 | java -jar snpEff.jar -c $BASE_DIR/snpEff.config -v GRCh38.p2.RefSeq > $BASE_DIR"/"$2

#java -jar snpEff.jar -c $BASE_DIR /snpEff.config -v > $BASE_DIR  "/" $2
#python snpeff_annotator.py | java -jar snpEff.jar -c ./snpEff.config -v GRCh38.p2.RefSeq > test.GRCh38.chr22.vcf
