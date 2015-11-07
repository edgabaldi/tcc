#coding:utf-8
from decimal import Decimal
import datetime
import json

from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone

from product.models import Product
from product.forms import ProductSearchForm
from account.models import User
from account.forms import SignUpModelForm
from core.views import SearchableListView, LoginRequiredMixin


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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboard.html'

class ProductMixin(object):
    def dispatch(self, *args, **kwargs):
        self.product = get_object_or_404(Product, id=kwargs['pk'])
        return super(ProductMixin, self).dispatch(*args, **kwargs)

class OpenClockView(ProductMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            self.product.open_clock()
            return HttpResponse(status=200)
        return HttpResponse(status=403)

class BidView(ProductMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'first_clock_limit': self.product.first_clock_limit(),
            'bids': map(
                lambda x: x.to_dict(),
                self.product.bids.order_by('-id'))
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self._create_bid(request)
        return HttpResponse('Authentication required', status=403)

    def _create_bid(self, request):
        body = json.loads(request.body)
        value = body.get('value')
        if not value:
            return HttpResponse('Bid needs a value', status=400)
        try:
            self.product.bids.create(value=Decimal(value), user=request.user)
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse('Bad request (%s)' % str(e), status=400)
