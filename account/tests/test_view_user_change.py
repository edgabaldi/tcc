from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy


class UserUpdateViewTestCase(TestCase):

    def setUp(self):
        self._setup_user()
        self.client.login(username='user', password='secret')

        self.url = reverse('user_edit', args=(10,))
        self._setup_user_to_edit()
        self.response = self.client.get(self.url)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'account/user_form.html')

    def test_post_form_valid(self):
        response = self.client.post(self.url, self._valid_dict())
        self.assertRedirects(response, reverse('user_list'))

    def test_post_form_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_valid())

    def _setup_user_to_edit(self):
        mommy.make(settings.AUTH_USER_MODEL, id=10)

    def _valid_dict(self):

        return {
            'username': 'foobar',
            'is_active': '1',
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@bar.com',
            'phone': 'xxx',
            'birth_date': '02/08/1986',
            'cpf_cnpj':'51763747654',
            'doc': '1234',
            'doc_entity': 'detran/rj',
            'address': '3rd street',
            'neighborhood': 'neighborhood',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'cep': '23000000',
        }

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='user',
            is_active=True)
        self.user.set_password('secret')
        self.user.save()
