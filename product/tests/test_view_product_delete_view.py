from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class ProductDeleteViewTestCase(TestCase):

    def setUp(self):
        mommy.make('product.Product', pk=22)
        self.url = reverse('product_delete', args=(22,))

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('product_list')) 
