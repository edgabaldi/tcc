from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy


class ActivateUserTestCase(TestCase):

    def setUp(self):
        mommy.make(settings.AUTH_USER_MODEL, id=10)
        self.url = reverse('activate_user', args=(10,))
        
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response,
                                'account/user_activate.html')

    def test_post_activate(self):
        response = self.client.post(self.url, {'is_active':True})
        self.assertRedirects(response, reverse('user_list'))

    def test_post_deactivate(self):
        response = self.client.post(self.url, {
            'is_active': False,
            'observation': 'Foo',
        })
        self.assertRedirects(response, reverse('user_list'))
