#coding:utf-8
from django.views.generic.edit import (CreateView, 
                                       UpdateView, 
                                       DeleteView)
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from core.views import SearchableListView
from product.models import Product
from product.forms import ProductSearchForm, ProductModelForm


class ProductSearchableListView(SearchableListView):
    """
    View that allow list and search products
    """
    model = Product
    template_name = 'product/product_list.html'
    paginate_by=25
    form_class = ProductSearchForm


class ProductActionMixin(object):
    """
    Common product attributs
    """
    model = Product
    form_class = ProductModelForm
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
    model = Product
    success_url = reverse_lazy('product_list')
