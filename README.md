# NCBI_August_Hackathon_Push_Button_Genomics_Solution

https://github.com/DCGenomics/NCBI_August_Hackathon_Push_Button_Genomics_Solution/wiki

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/DCGenomics/NCBI_August_Hackathon_Push_Button_Genomics_Solution?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Commands into SNP Eff to initialize databases for subsequent annotations were:

Though in principle we should probably add ALL databases provided at http://snpeff.sourceforge.net/ the following commands were used to annotate and download databases used by SnpEff:
 To select GRCh38.p2 as the ref
java -Xmx4G -jar snpEff.jar -c ./snpEff.config -v -lof GRCh38.p2.RefSeq.genome examples/test.GRCh38.vcf
Note: for this step, it may be necessary to add lines like the following to your snpEff.config if doing this on your local machine:
 Human genome GRCh38 using RefSeq transcripts
GRCh38.p2_genomic.genome : Homo_Sapiens
 GRCh38 release from NCBI's RefSeq 
GRCh38.p2.RefSeq.genome : Human genome GRCh38 using RefSeq transcripts

add dbsnp stuff
java -jar SnpSift.jar annotate -dbsnp test.GRCh38.vcf > test.GRCh38.dbsnp.chr22.vcf 
 add clinvar annotations
java -jar SnpSift.jar annotate -clinvar test.GRCh38.dbsnp.vcf > test.GRCh38.dbsnp.clinvar.vcf
add carlos's gff
java -Xmx4G -jar snpEff.jar -c ./snpEff.config -v -interval ./data/GGRCh38.p4_gene.gff test.GRCh38.dbsnp.clinvar.vcf > test.GRCh38.dbsnp.clinvar.gene.vcf
 add geneId
java -jar r test.GRCh38.dbsnp.vcf > test.GRCh38.dbsnp.clinvar.vcf

