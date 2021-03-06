from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy



class HelpViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('help')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'website/help.html')
