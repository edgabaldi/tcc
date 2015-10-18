from mock import patch

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from website.views import SignUpCreateView


class SignUpCreateViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

    def test_url(self):
        self.assertEqual('/cadastrar/', reverse('signup'))

    def test_get(self):
        response = SignUpCreateView.as_view()(self.request)
        self.assertEqual(200, response.status_code)

    @patch('website.views.messages')
    def test_post_form_valid(self, messages):
        messages.info.return_value=None
        self._setup_form_valid()
        request = self.factory.post('/', data = self.data)
        response = SignUpCreateView.as_view()(request)
        self.assertEqual(302, response.status_code)

    def test_post_form_invalid(self):
        request = self.factory.post('/')
        response = SignUpCreateView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def _setup_form_valid(self):

        self.data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@bar.com',
            'phone': '12345',
            'birth_date': '10/10/2015',
            'cpf_cnpj': '12345687',
            'doc': '123',
            'doc_entity': 'foo',
            'address': 'foo',
            'neighborhood': 'bar',
            'city': 'Manaus',
            'state': 'RJ',
            'cep': 'foo',
            'username': 'alfa',
            'password': 'secret',
            'repeat_password': 'secret',
            'accepted_terms': '1',
        }
 
