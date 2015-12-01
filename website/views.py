#coding:utf-8
from decimal import Decimal
import datetime
import json

from django.shortcuts import render_to_response, redirect
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

from product.models import Product, Bid, Photo
from product.forms import ProductSearchForm
from account.models import User
from account.forms import SignUpModelForm
from core.views import SearchableListView, LoginRequiredMixin, MenuActiveMixin
from recommender.models import ProductSimilarity


class ProductListView(MenuActiveMixin, SearchableListView):
    menu_active='index'
    template_name = 'website/index.html'
    model = Product
    form_class = ProductSearchForm
    paginate_by = 8


class ProductDetailView(MenuActiveMixin, DetailView):
    menu_active='index'
    template_name = 'website/product.html'
    model = Product

    def get_similar_products(self):
        return ProductSimilarity.objects.select_related('similar').filter(
            reference=self.object.reference).order_by('-score')[:8]

    def get_context_data(self, **kwargs):
        return super(ProductDetailView, self).get_context_data(
            similars = self.get_similar_products(),
            **kwargs)


class SignUpCreateView(MenuActiveMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpModelForm
    template_name = 'website/signup.html'
    menu_active = 'signup'
    success_url = reverse_lazy('index')
    success_message = u'Usuário Cadastrado, Aguarde a ativação!'

    def form_valid(self, form):
        passwd = form.cleaned_data.get('password')
        self.object = form.save()
        self.object.set_password(passwd)
        self.object.save()
        return redirect(self.get_success_url())


class DashboardView(MenuActiveMixin, LoginRequiredMixin, TemplateView):
    menu_active = 'dashboard'
    template_name = 'website/dashboard.html'

    def get_dashboard_stats(self):

        return {
            'user_count': User.objects.count(),
            'product_count': Product.objects.count(),
            'bid_count': Bid.objects.count(),
            'photo_count': Photo.objects.count(),
        }

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update(self.get_dashboard_stats())
        return context

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


class HelpView(MenuActiveMixin, TemplateView):
    menu_active='help'
    template_name='website/help.html'
