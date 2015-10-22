# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='depot',
            field=models.CharField(default=b'N/I', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='fuel',
            field=models.CharField(default=b'N/I', max_length=50),
        ),
        migrations.AlterField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(related_name='bids', to='product.Product'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='model',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
