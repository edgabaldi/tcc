from unittest import skip

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from account.views import AccountListView


class AccountListViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_url(self):
        self.assertEqual('/account/', 
                         reverse('account_list'))

    def test_get(self):
        response = AccountListView.as_view()(self.request)
        self.assertEqual(200, response.status_code)

    @skip('verify')
    def test_template_used(self):
        response = AccountListView.as_view()(self.request)
        self.assertIn('account/account_list.html', 
                      response.template_name)
