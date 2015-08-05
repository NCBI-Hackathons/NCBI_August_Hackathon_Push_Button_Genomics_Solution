import os, sys

filter_param=sys.argv[1]
filter_param=str.lower(filter_param)
print filter_param

if filter_param=="missense":
	input_param="\"ANN[0].EFFECT has 'missense_variant'\""

try:
	if isinstance( int(filter_param), int ):
		input_param="\" (CLNSIG ==" + filter_param + ")\""
except ValueError:
	pass

print input_param

os.system("java -jar SnpSift.jar filter " + input_param + " /home/ubuntu/segun/snakemake.testrun/results/dummy_1.anno.vcf > filtered.anno.vcf")
