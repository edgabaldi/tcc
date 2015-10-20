from unittest import skip

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy


class UserUpdateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('user_edit', args=(10,))
        self._setup_user()
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    @skip('todo')
    def test_post(self):
        pass

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'account/user_form.html')

    def _setup_user(self):
        mommy.make(settings.AUTH_USER_MODEL, id=10)

