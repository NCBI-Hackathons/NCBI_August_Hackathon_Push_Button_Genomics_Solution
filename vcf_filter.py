import os, sys

filter_param=sys.argv[1]


try:
	if isinstance( int(filter_param), int ):
#		input_param="\" (CLNSIG=" + filter_param + ")\""
		os.system("grep \"\#\" /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.vcf  > /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.filtered.vcf")
		os.system("grep \"CLNSIG=5\" /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.vcf  >> /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.filtered.vcf")
except ValueError:
	pass

filter_param=str.lower(filter_param)
print filter_param

if filter_param=="missense":
	input_param="\"ANN[0].EFFECT has 'missense_variant'\""
	os.system("java -jar /home/ubuntu/vlaufer/snpeff/snpEff/NCBI_August_Hackathon_Push_Button_Genomics_Solution/SnpSift.jar filter " + input_param + " /home/ubuntu/segun/snakemake.testrun/results/dummy_1.anno.vcf > /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.filtered.vcf")



"""
# accept arguments
filter_param=sys.argv[1]
input_file=sys.argv[2]
output_file=sys.argv[3]

#print output_file
#/home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.vcf
#/home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.filtered.vcf

filter_param=str.lower(filter_param)
#print filter_param

arg=filter_param + " " + input_file + " > " +  output_file

if filter_param=="missense":
	input_param="\"ANN[0].EFFECT has 'missense_variant'\""
	print input_param
	os.system("java -jar SnpSift.jar filter \" + input_param + \" /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.vcf > /home/ubuntu/segun/snakemake.testrun/results/dummy_1.annotated.filtered.vcf")

try:
	if isinstance( int(filter_param), int ):
		input_param="\" ( CLNSIG=" + filter_param + " )\""
		os.system("grep \"\#\" + input_file + \" >> \" + output_file)
		os.system("grep \"CLNSIG=5\" + input_file +  \" >> \" output_file)
except ValueError:
	pass

"""
