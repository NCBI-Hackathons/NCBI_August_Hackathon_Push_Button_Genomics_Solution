# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='chrom',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gene',
            name='end',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gene',
            name='gene_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gene',
            name='gene_name_upper',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gene',
            name='start',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gene',
            name='strand',
            field=models.CharField(default='+', max_length=1),
            preserve_default=False,
        ),
    ]
