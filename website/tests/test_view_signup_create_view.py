from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from website.views import SignUpCreateView


class SignUpCreateViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_url(self):
        self.assertEqual('/cadastrar/', reverse('signup'))

    def test_get(self):
        response = SignUpCreateView.as_view()(self.request)
        self.assertEqual(200, response.status_code)
