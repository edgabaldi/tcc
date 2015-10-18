# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField()),
                ('brand', models.ForeignKey(to='product.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=150)),
                ('color', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=15)),
                ('product_number', models.PositiveIntegerField()),
                ('initial_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('general_state', models.CharField(max_length=20, choices=[(b'veiculo', 'VE\xcdCULO'), (b'veiculo_sem_motor', 'VE\xcdCULO SEM MOTOR'), (b'sucata', 'SUCATA')])),
                ('clock_starts_at', models.DateTimeField()),
                ('status', models.CharField(max_length=20, choices=[(b'loteamento', 'EM LOTEAMENTO'), (b'liberado_lance', 'LIBERADO PARA LANCE'), (b'encerrado', 'ENCERRADO')])),
                ('reference', models.CharField(max_length=150)),
                ('model', models.ForeignKey(to='product.Model')),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(to='product.Product'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
