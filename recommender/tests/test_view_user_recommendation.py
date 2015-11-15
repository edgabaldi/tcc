from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy


class UserRecommendationViewTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL,
            username = 'user',
            is_active=True)
        self.user.set_password('secret')
        self.user.save()

        self.client.login(username='user', password='secret')


    def test_get(self):
        self.url = reverse('user_recommendation')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
