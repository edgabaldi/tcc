from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse

from core.views import LoginRequiredMixin

from model_mommy import mommy

class FakeUser(object):

    def __init__(self, is_authenticated=False):
        self._is_authenticated=is_authenticated

    def is_authenticated(self):
        return self._is_authenticated

class DummyLoginRequiredView(LoginRequiredMixin, View):

    def get(self, request):
        return HttpResponse('ok')


class LoginRequiredMixinTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_get_authenticated(self):
        self.request.user = FakeUser(is_authenticated=True)
        response = DummyLoginRequiredView.as_view()(self.request)
        self.assertEqual(200, response.status_code)

    @patch('core.views.messages')
    def test_get_not_authenticated(self, _messages):
        self.request.user = FakeUser(is_authenticated=False)
        response = DummyLoginRequiredView.as_view()(self.request)
        self.assertEqual(302, response.status_code)
        self.assertTrue(_messages.warning.called)
