# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsimilarity',
            name='is_similar_to',
            field=models.ForeignKey(to='product.Product'),
        ),
        migrations.AlterField(
            model_name='productsimilarity',
            name='product',
            field=models.ForeignKey(related_name='similars', to='product.Product'),
        ),
    ]
