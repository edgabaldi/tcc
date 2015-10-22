# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20151022_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='clock_starts_at',
            field=models.DateTimeField(null=True),
        ),
    ]
