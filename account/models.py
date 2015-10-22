#coding:utf-8
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin,)

STATE_CHOICES = (
    ('RJ', 'Rio de Janeiro'),
)

now = timezone.now()

class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):

        user = self.model(username=username, 
                          last_login=now,
                          **extra_fields)
        user.set_password(user)
        user.save()

    def create_user(self, username, password, **extra_fields):

        extra_fields.update(is_active=False, is_superuser=False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):

        extra_fields = {
            'first_name': 'Admin',
            'last_name': 'Instrator',
            'phone': 'foo',
            'birth_date' : now,
            'cpf_cnpj': '11111111111',
            'doc': '',
            'doc_entity': '',
            'city': 'Rio de Janeiro',
            'neighborhood': 'Recreio',
            'state': 'RJ',
            'cep':'23000-000',
            'is_superuser': True,
            'is_active': True,
        }

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'username'

    username = models.CharField(u'Usuário', max_length=40, unique=True)

    first_name = models.CharField('Primeiro Nome',max_length=50)
    last_name = models.CharField('Ultimo Nome', max_length=50)
    email = models.CharField('Email', max_length=255)
    phone = models.CharField('Telefone', max_length=30)
    birth_date = models.DateField('Data de Nascimento')
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=15)
    doc = models.CharField('Identidade', max_length=20, blank=True)
    doc_entity = models.CharField('Orgão Expedidor', max_length=20, blank=True)
    address = models.CharField('Endereço', max_length=200)
    city = models.CharField('Cidade', max_length=100)
    neighborhood = models.CharField('Bairro', max_length=100)
    state = models.CharField('Estado', max_length=2, choices=STATE_CHOICES)
    cep = models.CharField('CEP', max_length=10)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_marketing = models.BooleanField(default=False)

    objects = UserManager()

    def __unicode__(self):
        return self.username
