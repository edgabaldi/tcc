from django.test import TestCase

from django.core.urlresolvers import reverse


class UserRecommendationViewTestCase(TestCase):

    def test_get(self):
        self.url = reverse('user_recommendation')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
