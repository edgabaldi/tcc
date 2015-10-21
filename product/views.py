#coding:utf-8
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from core.views import SearchableListView
from product import models
from product import forms

#
# Product Views
#


class ProductSearchableListView(SearchableListView):
    """
    View that allow list and search products
    """
    model = models.Product
    template_name = 'product/product_list.html'
    paginate_by=25
    form_class = forms.ProductSearchForm


class ProductActionMixin(object):
    """
    Common product attributs
    """
    model = models.Product
    form_class = forms.ProductModelForm
    template_name='product/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductCreateView(ProductActionMixin, CreateView):
    """
    View that allow create new products
    """


class ProductUpdateView(ProductActionMixin, UpdateView):
    """
    View that allow update products
    """

class ProductDeleteView(DeleteView):
    model = models.Product
    success_url = reverse_lazy('product_list')


#
# Brand Views
#


class BrandSearchableListView(SearchableListView):
    """
    View that allow list and search brands
    """
    model = models.Brand
    template_name = 'product/brand_list.html'
    paginate_by=25
    form_class = forms.BrandSearchForm


class BrandActionMixin(object):
    """
    Commum attributes for Brand Edit Views
    """
    model = models.Brand
    template_name = 'product/brand_form.html'
    form_class = forms.BrandModelForm
    success_url = reverse_lazy('brand_list')


class BrandCreateView(BrandActionMixin, CreateView):
    """
    View that allow create new brands
    """


class BrandUpdateView(BrandActionMixin, UpdateView):
    """
    View that allow change brands
    """


#
# Model Views
#


class ModelSearchableListView(SearchableListView):
    """
    View that allow list and search models
    """
    model = models.Model
    template_name = 'product/model_list.html'
    paginate_by=25
    form_class = forms.ModelSearchForm


class ModelCreateView(CreateView):
    """
    View that allow create new models
    """
    model = models.Model
    template_name = 'product/model_form.html'
    form_class = forms.ModelModelForm
    success_url = reverse_lazy('model_list')

