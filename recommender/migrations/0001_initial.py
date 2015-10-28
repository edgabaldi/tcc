# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20151022_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSimilarity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=6, decimal_places=5)),
                ('is_similar_to', models.ForeignKey(related_name='similars', to='product.Product')),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
    ]
