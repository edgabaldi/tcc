from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class ProductUpdateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('product_edit', args=(15,))
        self._setup_product()
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'product/product_form.html')

    @skip('todo')
    def test_post(self):
        pass



    def _setup_product(self):
        mommy.make('product.Product', id=15)

