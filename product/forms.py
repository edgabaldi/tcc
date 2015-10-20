#coding:utf-8
from django import forms

from core.forms import BaseSearchForm
from product.models import Product, Model, GENERAL_STATE_CHOICES


class ProductSearchForm(BaseSearchForm):

    product_number = forms.IntegerField(
        label='Número do Lote',
        required=False)

    description = forms.CharField(
        max_length=50,
        label='Descrição',
        required=False)

    general_state = forms.CharField(
        max_length=20,
        widget=forms.Select(choices=GENERAL_STATE_CHOICES), 
        required=False, 
        label='Estado Geral')


    class Meta:
        queryset = Product.objects


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('model', 'description', 'color', 'year', 
                  'product_number', 'initial_price', 
                  'general_state', 'clock_starts_at', 'status',)

    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        query_optimized = Model.objects.select_related('brand').order_by('brand', 'name')
        self.fields['model'].queryset = query_optimized
