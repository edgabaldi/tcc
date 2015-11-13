from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy


class ProductUpdateViewTestCase(TestCase):

    def setUp(self):
        self._setup_user()
        self.client.login(username='user', password='secret')

        self.url = reverse('product_edit', args=(15,))
        self._setup_product()
        self.response = self.client.get(self.url)

        self.inline_dict = {
            'photo_set-TOTAL_FORMS':'3',
            'photo_set-INITIAL_FORMS':'0',
            'photo_set-MAX_NUM_FORMS':'1000',
            'photo_set-MIN_NUM_FORMS':'0',
            'photo_set-0-file':'',
            'photo_set-1-file':'',
            'photo_set-2-file':'',
        }

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response,
                                'product/product_form.html')

    def test_post_form_valid(self):
        self._setup_post()
        response = self.client.post(self.url, self.valid_dict)
        self.assertRedirects(response, reverse('product_list'))

    def test_post_form_invalid(self):
        response = self.client.post(self.url, self.inline_dict)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_valid())

    def _setup_post(self):

        mommy.make('product.Model', pk=1)

        self.valid_dict = {
            'description': 'A description',
            'model':'1',
            'color':'Azul',
            'year':'2010/2010',
            'product_number':'10',
            'general_state':'veiculo',
            'initial_price': '1234.50',
            'clock_opened_at': '16/10/2015 10:00:00',
            'status':'loteamento'
        }

        self.valid_dict.update(self.inline_dict)

    def _setup_product(self):
        mommy.make('product.Product', id=15)

    def _setup_user(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='user',
            is_active=True)
        self.user.set_password('secret')
        self.user.save()
