from django.db import models

class Gene(models.Model):
    """
    `Gene` model
    """
    # entrez id
    slug = models.SlugField()

class GeneUserData(models.Model):
    """
    `GeneUserData` model
    """
    # hash
    upload_hash = models.CharField(max_length=6)

    # foreign key to gene
    gene = models.ForeignKey(to=Gene, related_name='gene_user_data')
