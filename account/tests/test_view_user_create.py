from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse


class UserCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('user_add')
        self.response = self.client.get(self.url)
        
    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'account/user_form.html')

    @skip('todo')
    def test_post(self):
        pass


