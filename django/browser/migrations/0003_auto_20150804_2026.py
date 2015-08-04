# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0002_auto_20150804_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gene',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
