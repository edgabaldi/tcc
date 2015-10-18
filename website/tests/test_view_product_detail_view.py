from django.test import TestCase
from django.test.client import RequestFactory

from website.views import ProductDetailView

from model_mommy import mommy


class ProductDetailViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def _setup_product(self):
        mommy.make('product.Product', pk=10)

    def test_get(self):
        self._setup_product()
        resp = ProductDetailView.as_view()(self.request, pk=10)
        self.assertEqual(200, resp.status_code)
