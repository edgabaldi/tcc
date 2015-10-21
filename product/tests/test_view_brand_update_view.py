from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class BrandUpdateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('brand_edit', args=(18,))
        self._setup_brand()
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'product/brand_form.html')

    def test_post_form_valid(self):
        valid_dict = {'name':'Ferrari'}
        response = self.client.post(self.url, valid_dict)
        self.assertRedirects(response, reverse('brand_list'))

    def _setup_brand(self):
        mommy.make('product.Brand', id=18)

