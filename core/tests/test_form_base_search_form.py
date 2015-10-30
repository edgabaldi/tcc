from django.test import TestCase
from django import forms

from core.forms import BaseSearchForm
from product.models import (Product, GENERAL_STATE_CHOICES,
                            Brand, Model)

from model_mommy import mommy


class ProductSearchForm(BaseSearchForm):

    product_number = forms.IntegerField(required=False)

    model__brand = forms.ModelChoiceField(
        queryset = Brand.objects.all(),
        required=False)

    model = forms.ModelChoiceField(
        queryset = Model.objects.select_related('brand'),
        required=False)

    general_state = forms.CharField(
        max_length=20,
        widget=forms.Select(choices=GENERAL_STATE_CHOICES), 
        required=False) 

    class Meta:
        queryset = Product.objects


class ProductSearchFormTestCase(TestCase):
    """
    Test a BaseSearchForm
    """

    def setUp(self):

        self.product = mommy.make(
            'product.Product',
            product_number = 1234,
            brand__id=1,
            model__id=1,
            general_state='veiculo')

    def test_empty_search(self):
        answer = self._search_by({
            'product_number':'',
            'brand':'',
            'model':'',
            'general_state':''})

        self.assertTrue(answer)

    def test_search_by_product_number(self):

        answer = self._search_by({
            'product_number':'1234',
            'brand':'',
            'model':'',
            'general_state':''})

        self.assertTrue(answer)

    def test_search_by_brand(self):

        answer = self._search_by({
            'product_number':'',
            'model__brand':'1',
            'model':'',
            'general_state':''})

        self.assertTrue(answer)

    def test_search_by_model(self):

        answer = self._search_by({
            'product_number':'',
            'model__brand':'',
            'model':'1',
            'general_state':''})

        self.assertTrue(answer)


    def test_search_by_general_state(self):

        answer = self._search_by({
            'product_number':'',
            'model__brand':'',
            'model':'',
            'general_state':'veiculo'})

        self.assertTrue(answer)

    def test_search_all_field_filled(self):

        answer = self._search_by({
            'product_number':'1234',
            'model__brand':'1',
            'model':'1',
            'general_state':'veiculo'})

        self.assertTrue(answer)

    def _search_by(self, form_dict):

        form = ProductSearchForm(form_dict)

        self.assertTrue(form.is_valid())

        result = form.get_result_queryset()

        self.assertEqual([self.product], list(result))

        return True

