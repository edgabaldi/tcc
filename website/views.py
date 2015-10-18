#coding:utf-8
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from product.models import Product
from account.models import User
from account.forms import SignUpModelForm


class ProductListView(ListView):
    template_name = 'website/index.html'
    model = Product
    paginate_by = 8


class ProductDetailView(DetailView):
    template_name = 'website/product.html'
    model = Product


class SignUpCreateView(CreateView):
    model = User
    form_class = SignUpModelForm
    template_name = 'website/signup.html'
    success_url = reverse_lazy('index')
    success_msg = u'Usuário Cadastrado, Aguarde a ativação!'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(SignUpCreateView, self).form_valid(form)


def login(request):
    return render_to_response('website/login.html')

def dashboard(request):
    return render_to_response('website/dashboard.html')
