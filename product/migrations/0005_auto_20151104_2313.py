# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20151022_0215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='clock_starts_at',
        ),
        migrations.AddField(
            model_name='bid',
            name='closes_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='clock_opened_at',
            field=models.DateTimeField(null=True),
        ),
    ]
