#!/usr/bin/env Rscript

directory <- commandArgs(T)
print(directory)

VCF_one_line_impact <- function(directory){
	
	# Import tables for amino acids
	list_3_1_letter_code <- read.table('list_3_1_letter_code.txt', stringsAsFactors = FALSE, sep="\t", header=T)
	Additional_impact_score_missense <- read.table('Additional_impact_score_missense_and_reverse.txt', stringsAsFactors = FALSE, sep="\t", header=T, na.strings="truc")
	
	# Create lists to get the amino acids with p."aa" and "aa"|
	list_aapipe <- paste(list_3_1_letter_code[,1], "|", sep="")
	list_3_1_letter_code[,3] <- paste("p.",list_3_1_letter_code[,1], sep="")
	list_3_1_letter_code[,4] <- paste(list_3_1_letter_code[,1], "|", sep="")
	
	# Import vcf
	VCF_file_input <- read.table(directory, stringsAsFactors = FALSE, sep="\t")
	VCF_file_output <- VCF_file_input
	
	# Find column with missense
	list_row_missense <- grep("missense_variant", VCF_file_input[,8])
	
	# Get the aa and add the change at the end of the line
	for(i in list_row_missense){
		for(p.aa in list_3_1_letter_code[,3]){
			if(grepl(p.aa, VCF_file_input[i,8])){
				origin <- p.aa
			}
		}
		for(aapipe in list_3_1_letter_code[,4]){
			if(grepl(aapipe, VCF_file_input[i,8], fixed=T)){
				change <- aapipe
			}
		}
		aa_changed <- paste(list_3_1_letter_code[list_3_1_letter_code[,3]==origin,2], list_3_1_letter_code[list_3_1_letter_code[,4]==change,2], sep = "")
		if(aa_changed %in% Additional_impact_score_missense[,1]){
			Impact <- Additional_impact_score_missense[Additional_impact_score_missense[,1]==aa_changed,3]
		} else if(aa_changed %in% Additional_impact_score_missense[,2]){
			Impact <- Additional_impact_score_missense[Additional_impact_score_missense[,2]==aa_changed,3]
		} else{
			Impact <- NA
		}
		
		VCF_file_output[i,8] <- paste(VCF_file_input[i,8],";IMPACT=",Impact,sep="")
	}
write.table(VCF_file_output, paste("./impact_",directory,sep=""), quote=F, sep="\t", row.names=F, col.names=F)
}

VCF_one_line_impact(directory)