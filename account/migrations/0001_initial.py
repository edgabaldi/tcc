# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=40, verbose_name='Usu\xe1rio')),
                ('first_name', models.CharField(max_length=50, verbose_name=b'Primeiro Nome')),
                ('last_name', models.CharField(max_length=50, verbose_name=b'Ultimo Nome')),
                ('email', models.CharField(max_length=255, verbose_name=b'Email')),
                ('phone', models.CharField(max_length=30, verbose_name=b'Telefone')),
                ('birth_date', models.DateField(verbose_name=b'Data de Nascimento')),
                ('cpf_cnpj', models.CharField(max_length=15, verbose_name=b'CPF/CNPJ')),
                ('doc', models.CharField(max_length=20, verbose_name=b'Identidade', blank=True)),
                ('doc_entity', models.CharField(max_length=20, verbose_name=b'Org\xc3\xa3o Expedidor', blank=True)),
                ('address', models.CharField(max_length=200, verbose_name=b'Endere\xc3\xa7o')),
                ('city', models.CharField(max_length=100, verbose_name=b'Cidade')),
                ('neighborhood', models.CharField(max_length=100, verbose_name=b'Bairro')),
                ('state', models.CharField(max_length=2, verbose_name=b'Estado', choices=[(b'RJ', b'Rio de Janeiro')])),
                ('cep', models.CharField(max_length=10, verbose_name=b'CEP')),
                ('is_active', models.BooleanField(default=False)),
                ('accepted_terms', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
