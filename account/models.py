from django.db import models
from django.contrib.auth.models import AbstractBaseUser

STATE_CHOICES = (
    ('RJ', 'Rio de Janeiro'),
)

class User(AbstractBaseUser):

    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    birth_date = models.DateField()
    cpf_cnpj = models.CharField(max_length=15)
    doc = models.CharField(max_length=20)
    doc_entity = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)
    old_id = models.PositiveIntegerField()

    def __unicode__(self):
        return self.username
