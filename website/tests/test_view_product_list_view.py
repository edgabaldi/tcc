from django.test import TestCase
from django.core.urlresolvers import reverse

from website.views import ProductListView


class ProductListViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('index')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'website/index.html')
