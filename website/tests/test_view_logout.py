from django.test import TestCase
from django.core.urlresolvers import reverse


class LoginViewTestCase(TestCase):

    def setUp(self):

        self.url = reverse('logout')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))
