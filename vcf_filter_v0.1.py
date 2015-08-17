######## Purpose of this script is to filter the vcf file using SNPEff according to user input #########

### Helpful documentation ###
## http://snpeff.sourceforge.net/SnpSift.html

#import modules
import os, sys
import subprocess

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
op="( "
cp=" )"
op=""
cp=""
quotation="\""
and_operator= " & "
or_operator= " | "

# input and output file names and paths
file_path=" /home/ubuntu/segun/snakemake.testrun/results/"
input_vcf= file_prefix + ".annotated.vcf "
output_vcf=file_prefix + ".annotated.filtered.vcf "

variant_types=["SNV","Insertion","Deletion","Indel"]
effect_types=["missense", "nonsense","synonymous","frameshift"]
impact_types=["LOW","MODERATE","SEVERE"]

#class snpsift_input_maker():
def variant_type_selector(arg):
	input_parameters=[]
	i=0
	input_file_path=file_path + input_vcf
	for filtering_param in filter_arguments:		
		i+=1
		if filtering_param in effect_types:
#			input_param="ANN[0].EFFECT has \'" + filtering_param + "_variant\'"
			input_param="\"ANN[0].EFFECT has \'" + filtering_param + "_variant\'\""
			input_parameters.append(input_param)
		elif filtering_param in impact_types:
        	        input_param="\"ANN[0].IMPACT = \'" + filtering_param + "\'\""
			input_parameters.append(input_param)
		elif filtering_param in variant_types:
                        input_param="\"VC = \'" + filtering_param + "\'\""
                        input_parameters.append(input_param)

		if i<len(effect_types):
		        temp_output_file_path=file_path + "temp." + str(i) + output_vcf
                        os.system(echo_cmd + opening_cmd + input_param + input_file_path + carat_cmd + temp_output_file_path + close_cmd) # echo the cmd to see output
                        os.system(opening_cmd + input_param + input_file_path + carat_cmd + temp_output_file_path)
		elif i==len(effect_types):
			try:
				os.system(echo_cmd + opening_cmd + input_param + input_file_path + carat_cmd + temp_output_file_path + close_cmd) # echo the cmd to see output
				os.system(opening_cmd + input_param + input_file_path + carat_cmd + temp_output_file_path)
			except:
				output_file_path=file_path + output_vcf
 				os.system(echo_cmd + opening_cmd + input_param + input_file_path + carat_cmd + output_file_path + close_cmd) # echo the cmd to see output
				os.system(opening_cmd + input_param + input_file_path + carat_cmd + output_file_path)

		input_file_path=temp_output_file_path

variant_type_selector(filter_arguments)




#	final_input=""
#	for input in input_parameters:
#		final_input=final_input + op + input + cp + and_operator
#	final_input=final_input[:-2]
#	final_input=final_input
#	print final_input

#	subprocess.call([opening_cmd, final_input, input_file_path, carat_cmd, output_file_path, close_cmd], shell="TRUE")



## Works
#######sts=subprocess.call("ls" + " -a", shell="TRUE" )
#	print([opening_cmd, input_param, input_file_path, carat_cmd, output_file_path, close_cmd])
#	cmd=subprocess.call([opening_cmd, input_param, input_file_path, carat_cmd, output_file_path, close_cmd], shell="False")


## Currently does not work with final_input
#	os.system(echo_cmd + opening_cmd + final_input + input_file_path + carat_cmd + output_file_path + close_cmd) # echo the cmd to see output
#	os.system(opening_cmd + final_input + input_file_path + carat_cmd + output_file_path)


#]	if isinstance( int(filter_param), int ):


## very helpful syntax examples here		
# http://snpeff.sourceforge.net/SnpSift.html#Extract
# ( EFF[*].EFFECT = 'NON_SYNONYMOUS_CODING' )
# ( CHROM = '22' ) & ( POS > 12345600 ) & ( POS < 43210000 )



########### For adding parsing based on ranges later
#### FUNCTIONAL STATMENT -->			input_param=" \" CHROM = \'" + filtering_param[0] + "\' \" "
#		elif filtering_param[0:5]=="CHROM":
#			filtering_param=filtering_param[5:]
#			filtering_param=filtering_param.split("-")
#			if len(filtering_param)==1:
#				input_param=" CHROM = \'" + filtering_param[0] +  "\' "
#			if len(filtering_param)==2:
#				input_param=" CHROM = \'" + filtering_param[0] + "\' " + cp
#				input_param=input_param + and_operator + op  + " POS > " + filtering_param[1]
#			print input_param
#
#			input_parameters.append(input_param)
#		elif 
