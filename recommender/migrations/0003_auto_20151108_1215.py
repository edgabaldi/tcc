# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20151104_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productsimilarity',
            old_name='is_similar_to',
            new_name='similar',
        ),
        migrations.RemoveField(
            model_name='productsimilarity',
            name='product',
        ),
        migrations.AddField(
            model_name='productsimilarity',
            name='reference',
            field=models.CharField(default='x', max_length=150),
            preserve_default=False,
        ),
    ]
