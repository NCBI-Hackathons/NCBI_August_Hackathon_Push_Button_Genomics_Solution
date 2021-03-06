#!/bin/bash

######## Purpose of this script is to filter the vcf file using SNPEff according to user input #########

### Helpful documentation ###
## http://snpeff.sourceforge.net/SnpSift.html

## Set variables for file paths
WRK_DIR="/home/ubuntu/vlaufer/snpeff/snpEff/NCBI_August_Hackathon_Push_Button_Genomics_Solution"
VCF_PATH="/home/ubuntu/segun/snakemake.testrun/results"
INFILE="$1"
INPUT_SUFFIX="annotated.vcf "
OUTPUT_SUFFIX="annotated.filtered.vcf "
OR_OPERATOR=" | "
AND_OPERATOR=" & "
OP_OP=" ("
CP_OP=" )"

## Set variables for the checkbox options
VARIANTS_TYPES=("SNV" "Insertion" "Deletion" "Indel")
EFFECT_TYPES=("missense" "nonsense" "synonymous" "frameshift")
IMPACT_TYPES=("LOW" "MODERATE" "SEVERE")

## Iterate through each argument fed to the script and classify it in order to deliver it to snpsift
for (( i=2; i<=$#; i++ )); do
	eval arg=\$$i

	for each in "${VARIANTS_TYPES[@]}"; do
		if [ "$arg" == "$each" ] ; then

			CMD="VC = '$arg'"
			if [[ -z "$VARIANT_CMD" ]]; then
				VARIANT_CMD="$CMD"
			else
				VARIANT_CMD="$VARIANT_CMD $OR_OPERATOR $CMD"
			fi
		fi
	done
	for each in "${EFFECT_TYPES[@]}"; do

		if [ "$arg" == "$each" ] ; then

                        CMD="ANN[0].EFFECT has '${arg}_variant'"
                        if [[ -z "$EFFECT_CMD" ]]; then
                                EFFECT_CMD="$CMD"
                        else
                                EFFECT_CMD="$EFFECT_CMD $OR_OPERATOR $CMD"
			fi

		fi
	done
	for each in "${IMPACT_TYPES[@]}"; do

		if [ "$arg" == "$each" ] ; then

                        CMD="ANN[0].IMPACT has '${arg}'"
                        if [[ -z "$IMPACT_CMD" ]]; then
                                IMPACT_CMD="$CMD"
                        else
                                IMPACT_CMD="$EFFECT_CMD $OR_OPERATOR $CMD"
			fi
		fi
	done
done

## Consider ((a|b) & (c)) & (d) vs ##(a|b) & (c) & (d)

# Construct the filter command
for facet in VARIANT_CMD EFFECT_CMD IMPACT_CMD; do
	eval CMD=\$$facet
	if [[ -z "$CMD" ]]; then
		echo "SKIP $facet"
	else
		CMD="$OP_OP $CMD $CP_OP "
		if [[ -z "$FILTER_CMD" ]]; then
			FILTER_CMD="$CMD"
		else
			FILTER_CMD="$FILTER_CMD $AND_OPERATOR $CMD"
		fi
	fi

done

# Now call snpsift
FILTER_CMD="$VARIANT_CMD" " $EFFECT_CMD"
echo Filter command is "$FILTER_CMD"
echo java -jar $WRK_DIR/SnpSift.jar filter " $FILTER_CMD " $VCF_PATH/$INFILE.$INPUT_SUFFIX
java -jar $WRK_DIR/SnpSift.jar filter " $FILTER_CMD " $VCF_PATH/$INFILE.$INPUT_SUFFIX  | grep -cv "^#"
java -jar $WRK_DIR/SnpSift.jar filter " $FILTER_CMD " $VCF_PATH/$INFILE.$INPUT_SUFFIX > $VCF_PATH/$INFILE.$OUTPUT_SUFFIX
