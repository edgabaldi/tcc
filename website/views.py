#coding:utf-8
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from product.models import Product
from product.forms import ProductSearchForm
from account.models import User
from account.forms import SignUpModelForm
from core.views import SearchableListView


class ProductListView(SearchableListView):
    template_name = 'website/index.html'
    model = Product
    form_class = ProductSearchForm
    paginate_by = 8


class ProductDetailView(DetailView):
    template_name = 'website/product.html'
    model = Product


class SignUpCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpModelForm
    template_name = 'website/signup.html'
    success_url = reverse_lazy('index')
    success_message = u'Usuário Cadastrado, Aguarde a ativação!'


def login(request):
    return render_to_response('website/login.html')

def dashboard(request):
    return render_to_response('website/dashboard.html')
