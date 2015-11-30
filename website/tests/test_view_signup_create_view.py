from django.test import TestCase
from django.core.urlresolvers import reverse

from website.views import SignUpCreateView


class SignUpCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'website/signup.html')

    def test_post_form_valid(self):
        self._setup_form_valid()
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse('index'))

    def test_post_form_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)


    def _setup_form_valid(self):

        self.data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@bar.com',
            'phone': '12345',
            'birth_date': '10/10/1990',
            'cpf_cnpj': '126.131.226-09',
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
 
