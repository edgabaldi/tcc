from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class ProductDetailViewTestCase(TestCase):

    def setUp(self):
        self._setup_product()
        self.url = reverse('product', args=(10,))
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 
                                'website/product.html') 

    def _setup_product(self):
        mommy.make('product.Product', pk=10)


