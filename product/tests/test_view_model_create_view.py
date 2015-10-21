from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class ModelCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('model_add')
        self.response = self.client.get(self.url)
        
    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'product/model_form.html')

    def test_post_form_valid(self):
        self._setup_fixture()
        valid_dict = {'name': 'Uni', 'brand':'16'}
        response = self.client.post(self.url, valid_dict)
        self.assertRedirects(response, reverse('model_list'))

    def test_post_form_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_valid())

    def _setup_fixture(self):
        mommy.make('product.Brand', pk=16)
