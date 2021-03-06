from django.db import models


class Gene(models.Model):
    """
    `Gene` model
    """
    # entrez id
    slug = models.SlugField(unique=True)

    # gene name upper
    gene_name_upper = models.CharField(max_length=30)

    # gene name display
    gene_name = models.CharField(max_length=30)

    # chrom
    chrom = models.CharField(max_length=20)

    # strand
    strand = models.CharField(max_length=1)

    # start
    start = models.IntegerField()

    # end
    end = models.IntegerField()

    @property
    def length(self):
        return self.end - self.start

    def __unicode__(self):
        return self.gene_name


class GeneUserData(models.Model):
    """
    `GeneUserData` model
    """
    # hash
    upload_hash = models.CharField(max_length=6)

    # foreign key to gene
    gene = models.ForeignKey(to=Gene, related_name='gene_user_data')

    def __unicode__(self):
        return self.upload_hash
