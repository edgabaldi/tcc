from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

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


def login(request):
    return render_to_response('website/login.html')

def dashboard(request):
    return render_to_response('website/dashboard.html')
