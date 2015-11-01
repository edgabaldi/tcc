from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from model_mommy import mommy

User = get_user_model()


class LoginViewTestCase(TestCase):

    def setUp(self):

        self.url = reverse('login')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_post_authentication_success(self):
        self._setup_user()
        response = self.client.post(self.url, {
            'username':'user', 'password':'secret'})
        self.assertEqual(200, response.status_code)
        self.assertTrue(self._user_is_authenticated(self.user))

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='user', 
            password='secret',
            is_active=True)

    def _user_is_authenticated(self, user):
        user = User.objects.get(pk=user.pk)
        return user.is_authenticated()



