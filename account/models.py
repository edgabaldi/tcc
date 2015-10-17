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
            'accepted_terms': True,
            'is_superuser': True,
            'is_active': True,
        }

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    birth_date = models.DateField()
    cpf_cnpj = models.CharField(max_length=15)
    doc = models.CharField(max_length=20, blank=True)
    doc_entity = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)

    objects = UserManager()

    def __unicode__(self):
        return self.username
