from django.test import TestCase
from django.test.client import RequestFactory

from website.views import ProductListView


class ProductListViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        request = self.factory.get('/')

        self.response = ProductListView.as_view()(request)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)
