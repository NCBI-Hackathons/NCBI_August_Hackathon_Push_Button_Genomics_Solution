######## Purpose of this script is to filter the vcf file using SNPEff according to user input #########

### Helpful documentation ###
## http://snpeff.sourceforge.net/SnpSift.html

#import modules
import os, sys

#Collect input as variables
i=0
file_prefix=sys.argv[1]
filter_arguments=[]

for arg in sys.argv:
	if i>1:
		filter_arguments.append(sys.argv[i])
	i+=1
print filter_arguments

# include the basic commands that will be present in every snpSift filter command
echo_cmd="echo \""
close_cmd=" \""

javacmd="java -jar "
snpsiftcmd=" /home/ubuntu/vlaufer/snpeff/snpEff/NCBI_August_Hackathon_Push_Button_Genomics_Solution/SnpSift.jar "
filter_cmd=" filter "
opening_cmd=javacmd + snpsiftcmd + filter_cmd
carat_cmd=" > "
op=" ( "
cp=" ) "
and_operator= " & "
or_operator= " | "

# input and output file names and paths
file_path=" /home/ubuntu/segun/snakemake.testrun/results/"
input_vcf= file_prefix + ".annotated.vcf "
output_vcf=file_prefix + ".annotated.filtered.vcf "

input_file_path=file_path + input_vcf
output_file_path=file_path + output_vcf
print input_file_path
print output_file_path


effect_types=["missense", "nonsense","synonymous"]
impact_types=["MODERATE","SEVERE"]

#class snpsift_input_maker():

def variant_type_selector(arg):
	input_parameters=[]
	for filtering_param in filter_arguments:
		if filtering_param in effect_types:
			input_param="\"ANN[0].EFFECT has \'" + filtering_param + "_variant\'\""
			input_parameters.append(input_param)
		elif filtering_param in impact_types:
        	        input_param="\"ANN[0].IMPACT = \'" + filtering_param + "\'\""
			input_parameters.append(input_param)

		else:
			pass

	final_input=""
	for input in input_parameters:
		final_input=final_input + op + input + cp + and_operator
	final_input=final_input[:-2]

	os.system(echo_cmd + opening_cmd + input_param + input_file_path + carat_cmd + output_file_path + close_cmd) # echo the cmd to see output
	os.system(opening_cmd + input_param + input_file_path + carat_cmd + output_file_path)


#]	if isinstance( int(filter_param), int ):


## very helpful syntax examples here		
# http://snpeff.sourceforge.net/SnpSift.html#Extract
# ( EFF[*].EFFECT = 'NON_SYNONYMOUS_CODING' )
# ( CHROM = '22' ) & ( POS > 12345600 ) & ( POS < 43210000 )

variant_type_selector(filter_arguments)


