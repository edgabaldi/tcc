from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy



class ProductListViewTestCase(TestCase):

    def setUp(self):
        self._setup_user()
        self.client.login(username='user', password='secret')

        self.url = reverse('dashboard')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'website/dashboard.html')

    def test_dashboard_stats_shoud_be_in_context(self):
        self.assertIn('product_count', self.response.context)
        self.assertIn('user_count', self.response.context)
        self.assertIn('bid_count', self.response.context)

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='user',
            is_active=True)
        self.user.set_password('secret')
        self.user.save()
