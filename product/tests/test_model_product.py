import datetime
from unittest import skip

from django.test import TestCase

from product.models import Product

from model_mommy import mommy


class ProductTestCase(TestCase):

    @skip('try this before import right data')
    def test_last_bid(self):
        self._setup_bids()
        self.assertEqual(self.last_bid, self.product.last_bid)

    def test_bid_count(self):
        self._setup_bids()
        self.assertEqual(2, self.product.bid_count)

    def test_generate_reference(self):
        self._setup_product()
        self.assertEqual('Foo+Bar+Baz', 
                         self.product._generate_reference())

    def test_generate_reference_on_save(self):
        self._setup_product()
        self.assertEqual('Foo+Bar+Baz', self.product.reference)

    def test_unicode(self):
        self._setup_product()
        self.assertEqual('Foo - Bar - Blz', str(self.product))

    def _setup_bids(self):

        self.product = mommy.make('product.Product')

        mommy.make('product.Bid', product=self.product,
                   created_at=datetime.datetime(2015,10,18,10,00))

        self.last_bid = mommy.make('product.Bid', 
           product=self.product,
           created_at=datetime.datetime(2015,10,18,11,00))

    def _setup_product(self):
        self.product = mommy.make('product.Product',
                                  model__brand__name='Foo',
                                  model__name='Bar',
                                  general_state='Baz',
                                  description='Blz')

