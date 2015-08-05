#!/bin/bash
    
BASE_DIR=`pwd`
#$2="test.GRCh38.dbsnp.chr22.vcf"  #placeholder for output annotated file
#python snpeff_annotator.py $BASE_DIR "/" $1 | java -jar snpEff.jar -c ./snpEff.config -v > $BASE_DIR  "/" $2
python annotation_initializer.py $1 | java -jar snpEff.jar -c $BASE_DIR/snpEff.config -v GRCh38.p2.RefSeq > $BASE_DIR"/"temp0.vcf

#add dbsnp stuff
java -jar SnpSift.jar annotate -dbsnp $BASE_DIR"/"temp0.vcf > $BASE_DIR"/"temp1.vcf 
# add clinvar annotations
java -jar SnpSift.jar annotate -clinvar $BASE_DIR"/"temp1.vcf > $2

