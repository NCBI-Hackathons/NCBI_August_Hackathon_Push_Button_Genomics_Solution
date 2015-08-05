#!/bin/bash

BASE_DIR=`pwd`
#$2="test.GRCh38.dbsnp.chr22.vcf"  #placeholder for output annotated file
#python snpeff_annotator.py $BASE_DIR "/" $1 | java -jar snpEff.jar -c ./snpEff.config -v > $BASE_DIR  "/" $2
python annotation_initializer.py $BASE_DIR"/"$1 | java -jar snpEff.jar -c $BASE_DIR/snpEff.config -v GRCh38.p2.RefSeq > $BASE_DIR"/"$2

#java -jar snpEff.jar -c $BASE_DIR /snpEff.config -v > $BASE_DIR  "/" $2
#python snpeff_annotator.py | java -jar snpEff.jar -c ./snpEff.config -v GRCh38.p2.RefSeq > test.GRCh38.chr22.vcf


#add dbsnp stuff
java -jar SnpSift.jar annotate -dbsnp $BASE_DIR"/"$2 > $BASE_DIR"/"temp.vcf 
# add clinvar annotations
java -jar SnpSift.jar annotate -clinvar $BASE_DIR"/"temp.vcf > $BASE_DIR"/"out.vcf
#add carlos's gff
#java -Xmx4G -jar snpEff.jar -c ./snpEff.config -v -interval ./data/GGRCh38.p4_gene.gff test.GRCh38.dbsnp.clinvar.chr22.vcf > test.GRCh38.dbsnp.clinvar.gene.chr22.vcf

