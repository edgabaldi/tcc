from django.shortcuts import render_to_response
from django.views.generic.list import ListView

from product.models import Product

class ProductListView(ListView):
    template_name = 'website/index.html'
    model = Product
    paginate_by = 8

index = ProductListView.as_view()


def product(request):
    return render_to_response('website/product.html')

def signin(request):
    return render_to_response('website/signin.html')

def login(request):
    return render_to_response('website/login.html')

def dashboard(request):
    return render_to_response('website/dashboard.html')
