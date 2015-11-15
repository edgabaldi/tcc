# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20151104_2313'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommender', '0003_auto_20151108_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSimilarity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=6, decimal_places=5)),
                ('product', models.ForeignKey(to='product.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='productsimilarity',
            name='similar',
            field=models.ForeignKey(related_name='similars', to='product.Product'),
        ),
    ]
