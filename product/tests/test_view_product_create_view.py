from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy


class ProductCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('product_add')
        self.response = self.client.get(self.url)
        
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
        response = self.client.post(self.url)
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
            'clock_starts_at': '16/10/2015 10:00:00',
            'status':'loteamento'
        }


