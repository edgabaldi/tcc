#coding:utf-8
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from core.views import SearchableListView, LoginRequiredMixin, MenuActiveMixin
from product import models
from product import forms

from extra_views import CreateWithInlinesView, UpdateWithInlinesView

#
# Product Views
#


class ProductSearchableListView(MenuActiveMixin, LoginRequiredMixin, 
                                SearchableListView):
    """
    View that allow list and search products
    """
    model = models.Product
    template_name = 'product/product_list.html'
    paginate_by=25
    form_class = forms.ProductSearchForm
    menu_active = 'dashboard'
    submenu_active = 'product'


class ProductActionMixin(LoginRequiredMixin, object):
    """
    Common product attributs
    """
    model = models.Product
    form_class = forms.ProductModelForm
    inlines = [forms.PhotoInline,]
    template_name='product/product_form.html'
    success_url = reverse_lazy('product_list')


class BaseProductActionMixin(MenuActiveMixin, ProductActionMixin, 
                             SuccessMessageMixin):
    """
    Mixin of ProductActionMixin with success messages
    """
    success_message = 'Produto salvo com sucesso.'
    menu_active = 'dashboard'
    submenu_active = 'product'


class ProductCreateView(BaseProductActionMixin, CreateWithInlinesView):
    """
    View that allow create new products
    """


class ProductUpdateView(BaseProductActionMixin, UpdateWithInlinesView):
    """
    View that allow update products
    """


class ProductDeleteView(MenuActiveMixin, LoginRequiredMixin, DeleteView):
    model = models.Product
    success_url = reverse_lazy('product_list')
    menu_active = 'dashboard'
    submenu_active = 'product'



#
# Brand Views
#


class BrandSearchableListView(MenuActiveMixin, LoginRequiredMixin, 
                              SearchableListView):
    """
    View that allow list and search brands
    """
    model = models.Brand
    template_name = 'product/brand_list.html'
    paginate_by=25
    form_class = forms.BrandSearchForm
    menu_active = 'dashboard'
    submenu_active = 'brand'



class BrandActionMixin(MenuActiveMixin, LoginRequiredMixin, object):
    """
    Commum attributes for Brand Edit Views
    """
    model = models.Brand
    template_name = 'product/brand_form.html'
    form_class = forms.BrandModelForm
    success_url = reverse_lazy('brand_list')
    menu_active = 'dashboard'
    submenu_active = 'brand'



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


class ModelSearchableListView(MenuActiveMixin, LoginRequiredMixin, 
                              SearchableListView):
    """
    View that allow list and search models
    """
    model = models.Model
    template_name = 'product/model_list.html'
    paginate_by=25
    form_class = forms.ModelSearchForm
    menu_active = 'dashboard'
    submenu_active = 'model'


class ModelActionMixin(MenuActiveMixin, LoginRequiredMixin, object):
    """
    Commum attributes for Model edit views
    """
    model = models.Model
    template_name = 'product/model_form.html'
    form_class = forms.ModelModelForm
    success_url = reverse_lazy('model_list')
    menu_active = 'dashboard'
    submenu_active = 'model'


class ModelCreateView(ModelActionMixin, CreateView):
    """
    View that allow create new models
    """


class ModelUpdateView(ModelActionMixin, UpdateView):
    """
    View that allow update models
    """
