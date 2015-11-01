#coding:utf-8
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from core.views import SearchableListView, LoginRequiredMixin
from product import models
from product import forms

from extra_views import CreateWithInlinesView, UpdateWithInlinesView

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
    inlines = [forms.PhotoInline,]
    template_name='product/product_form.html'
    success_url = reverse_lazy('product_list')


class BaseProductActionMixin(ProductActionMixin, SuccessMessageMixin):
    """
    Mixin of ProductActionMixin with success messages
    """
    success_message = 'Produto salvo com sucesso.'


class ProductCreateView(BaseProductActionMixin, CreateWithInlinesView):
    """
    View that allow create new products
    """


class ProductUpdateView(BaseProductActionMixin, UpdateWithInlinesView):
    """
    View that allow update products
    """


class ProductDeleteView(DeleteView):
    model = models.Product
    success_url = reverse_lazy('product_list')


#
# Brand Views
#


class BrandSearchableListView(LoginRequiredMixin, SearchableListView):
    """
    View that allow list and search brands
    """
    model = models.Brand
    template_name = 'product/brand_list.html'
    paginate_by=25
    form_class = forms.BrandSearchForm


class BrandActionMixin(LoginRequiredMixin, object):
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


class ModelActionMixin(object):
    """
    Commum attributes for Model edit views
    """
    model = models.Model
    template_name = 'product/model_form.html'
    form_class = forms.ModelModelForm
    success_url = reverse_lazy('model_list')


class ModelCreateView(ModelActionMixin, CreateView):
    """
    View that allow create new models
    """


class ModelUpdateView(ModelActionMixin, UpdateView):
    """
    View that allow update models
    """
