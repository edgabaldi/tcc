from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from website.views import ProductListView


class ProductListViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')

        self.response = ProductListView.as_view()(request)

    def test_url(self):
        self.assertEqual('/', reverse('index'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)
