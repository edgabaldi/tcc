#coding:utf-8
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

GENERAL_STATE_CHOICES = (
    ('veiculo', u'VEÍCULO'),
    ('veiculo_sem_motor', u'VEÍCULO SEM MOTOR'),
    ('sucata', u'SUCATA'),
)

STATUS_CHOICES = (
    ('loteamento', u'EM LOTEAMENTO'),
    ('liberado_lance', u'LIBERADO PARA LANCE'),
    ('encerrado', u'ENCERRADO'),
)


class Brand(models.Model):
    name = models.CharField('Nome', max_length=50)
    is_active = models.BooleanField(u'Está Ativo', default=True)

    def __unicode__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey('product.Brand', verbose_name='Marca')
    name = models.CharField('Nome', max_length=50)
    is_active = models.BooleanField(u'Está Ativo', default=True)

    def __unicode__(self):
        return u'{} - {}'.format(self.brand.name, self.name)


class Product(models.Model):

    model = models.ForeignKey('product.Model', verbose_name='Modelo')
    description = models.CharField('Descrição', max_length=150)
    color = models.CharField('Cor', max_length=100)
    year = models.CharField('Ano', max_length=15)
    fuel = models.CharField('Combustível', max_length=50, default='N/I')
    depot = models.CharField('Depósito', max_length=100, default='N/I')

    product_number = models.PositiveIntegerField('Número do Lote')
    initial_price = models.DecimalField('Preço Inicial', max_digits=10, decimal_places=2)
    general_state = models.CharField('Estado Geral', max_length=20, 
                                     choices=GENERAL_STATE_CHOICES)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    reference = models.CharField('Referência', max_length=150)
    clock_opened_at = models.DateTimeField('Data Abertura do Relógio', null=True)

    @property
    def last_bid(self):
        return self.bids.order_by('id').last()

    @property
    def bid_count(self):
        return self.bids.count()

    @property
    def photo_featured(self):
        return self.photo_set.first()

    def save(self, *args , **kwargs):
        self.reference = self._generate_reference()
        super(Product, self).save(*args, **kwargs)

    def open_clock(self):
        if not self.clock_opened_at:
            self.clock_opened_at = timezone.now()
            self.save()


    def first_clock_limit(self):
        if self.clock_opened_at:
            return self.clock_opened_at + datetime.timedelta(
                seconds=settings.CLOCK_SECONDS)


    def _generate_reference(self):
        return u'{}+{}+{}'.format(
            self.model.brand.name, 
            self.model.name, 
            self.general_state)

    def __unicode__(self):
        return '{} - {}'.format(self.model, self.description)


class Photo(models.Model):
    product = models.ForeignKey('product.Product', verbose_name='Produto')
    file = models.ImageField('Arquivo', upload_to='photos/')



class Bid(models.Model):
    user = models.ForeignKey('account.User', verbose_name='Usuário')
    product = models.ForeignKey('product.Product', related_name='bids', 
                                verbose_name='Produto',)
    value = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    closes_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.product.clock_opened_at and not self.closes_at:
            now = timezone.now()
            self.closes_at = now + datetime.timedelta(
                seconds=settings.CLOCK_SECONDS)
        return super(Bid, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'user_id' : self.user.id,
            'user_username' : self.user.username,
            'product_id':self.product.id,
            'value' : self.value,
            'id': self.id,
            'created_at' : self.created_at,
            'close_at' :self._get_closes_at()
        }

    def _get_closes_at(self):
        if self.closes_at:
            return self.closes_at
        if self.product.clock_opened_at:
            return self.product.first_clock_limit()

    def __unicode__(self):
        return '{} - {} - {}'.format(self.user, 
                                self.product.description,
                                self.value)

