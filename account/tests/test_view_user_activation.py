from mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from model_mommy import mommy

User = get_user_model()


class ActivateUserTestCase(TestCase):

    def setUp(self):
        self._setup_user()
        self.client.login(username='user', password='secret')

        self.user_to_active = mommy.make(
            settings.AUTH_USER_MODEL, id=10, is_active=False)
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
        self.assertTrue(self._get_user_is_active(self.user_to_active))

    def test_post_deactivate(self):
        response = self.client.post(self.url, {
            'is_active': False,
            'observation': 'Foo',
        })
        self.assertRedirects(response, reverse('user_list'))
        self.assertFalse(self._get_user_is_active(self.user_to_active))

    @patch('account.forms.ActivateUserModelForm.send_email_activate')
    def test_post_activate_send_email(self, _method):
        self.client.post(self.url, {'is_active':True})
        _method.assert_called_once_with(self.user_to_active)

    @patch('account.forms.ActivateUserModelForm.send_email_deactivate')
    def test_post_deactivate_send_email(self, _method):
        self.client.post(self.url, {
            'is_active':False, 
            'observation': 'Foo bar'
        })
        _method.assert_called_once_with(self.user_to_active)

    def _get_user_is_active(self, user):
        user = User.objects.get(id=user.id)
        return user.is_active

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='user',
            is_active=True)
        self.user.set_password('secret')
        self.user.save()
