from unittest import TestCase
from decimal import Decimal

from django.conf import settings

from website.forms import BidModelForm

from model_mommy import mommy


class BidModelFormTestCase(TestCase):
    
    def test_validation_withou_last_bid(self):
        self._setup_user()
        self._setup_product()

        form = BidModelForm({
            'product': '1',
            'user':'1',
            'value': '1510'
        })

        self.assertTrue(form.is_valid())

    def test_validation(self):
        self._setup_bid(value=Decimal('1500'))
        form = BidModelForm({
            'product': '1',
            'user':'1',
            'value': '1510'
        })
        self.assertTrue(form.is_valid())

    def test_max_value_validation(self):
        self._setup_bid(value=Decimal('1500'))
        form = BidModelForm({
            'product': '1',
            'user':'1',
            'value': '1500000'
        })
        self.assertFalse(form.is_valid())

    def test_min_value_validation(self):

        self._setup_bid(value=Decimal('1500'))
        form = BidModelForm({
            'product': '1',
            'user':'1',
            'value': '1500'
        })
        self.assertFalse(form.is_valid())

    def _setup_bid(self, value=None):
        self._setup_user()
        self._setup_product()
        self.bid = mommy.make('product.Bid',
                              product=self.product,
                              user = self.user,
                              value = value)

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL)
    
    def _setup_product(self):
        self.product = mommy.make(
            'product.Product',
            initial_price = Decimal('1500'))    
