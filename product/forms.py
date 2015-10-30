#coding:utf-8
from django import forms

from core.forms import BaseSearchForm
from product import models

from extra_views import InlineFormSet

#
# Product Forms
#

class ProductSearchForm(BaseSearchForm):

    product_number = forms.IntegerField(
        label='Número do Lote',
        required=False)

    brand = forms.ModelChoiceField(
        queryset = models.Brand.objects.all(),
        label='Marca',
        required=False)

    model = forms.ModelChoiceField(
        queryset = models.Model.objects.select_related('brand'),
        label='Model',
        required=False)

    general_state = forms.CharField(
        max_length=20,
        widget=forms.Select(choices=models.GENERAL_STATE_CHOICES), 
        required=False, 
        label='Estado Geral')


    class Meta:
        queryset = models.Product.objects


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ('model', 'description', 'color', 'year', 
                  'product_number', 'initial_price', 
                  'general_state', 'clock_starts_at', 'status',)

    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)
        query_optimized = models.Model.objects.select_related(
            'brand').order_by('brand', 'name')
        self.fields['model'].queryset = query_optimized


class PhotoInline(InlineFormSet):
    model = models.Photo
    extra=3


#
# Brand Forms
#


class BrandSearchForm(BaseSearchForm):

    name = forms.CharField(
        max_length=100,
        label='Nome',
        required=False,)

    class Meta:
        queryset = models.Brand.objects


class BrandModelForm(forms.ModelForm):

    class Meta:
        model = models.Brand
        fields = ('name',)


#
# Model Forms
#


class ModelSearchForm(BaseSearchForm):

    name = forms.CharField(
        max_length=100,
        label='Nome',
        required=False,)

    brand = forms.ModelChoiceField(
        queryset=models.Model.objects.select_related('brand'),
        required=False,
        label='Marca')


    class Meta:
        queryset = models.Model.objects


class ModelModelForm(forms.ModelForm):

    class Meta:
        model = models.Model
        fields = ('brand', 'name',)
