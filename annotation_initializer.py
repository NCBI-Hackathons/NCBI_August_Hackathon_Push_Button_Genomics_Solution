#!/usr/bin/env python


import sys

fin=sys.argv[1]

convertlist=[]
with open("GFF_files/ncbi_reference_sequence_to_chrnum.txt",'r') as convert:
	for line in convert:
		parts=line.strip().split('\t')
		convertlist.append(parts)

with open(fin) as infile:  
	
	for line in infile:
		parts=line.strip().split('\t')
		if parts[0][0:1]=='#':
			continue
		for chrnum, chraccnum in convertlist:
			if parts[0]==chraccnum:
				parts[0]=chrnum

		sys.stdout.write("\t".join(parts) + '\n')


