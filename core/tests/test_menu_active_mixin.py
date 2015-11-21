from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import View, TemplateView
from django.http import HttpResponse

from core.views import MenuActiveMixin


class MenuActiveMixinTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_get_menu_active_should_be_in_context(self):
        response = StubView.as_view()(self.request)
        self.assertEqual('my_beaultful_menu', 
                         response.context_data['menu_active'])

    def test_get_menu_active_without_menu_active_attr(self):
        response = InvalidStubView.as_view()(self.request)
        self.assertEqual(None, response.context_data['menu_active'])


class StubView(MenuActiveMixin, TemplateView):
    menu_active = 'my_beaultful_menu'
    template_name='base.html'


class InvalidStubView(MenuActiveMixin, TemplateView):
    template_name='base.html'
