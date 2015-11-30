import datetime

from django.test import SimpleTestCase

from account.forms import SignUpModelForm


class SignUpModelFormTestCase(SimpleTestCase):

    def test_validate_birth_date(self):
        """
        this validation is in a validator of model.
        """

        invalid_year = datetime.date.today().year - 16

        invalid_birth_date = datetime.date.today().replace(year=invalid_year)

        form = SignUpModelForm({
            'birth_date': invalid_birth_date
        })

        form.is_valid()

        self.assertIn('birth_date', form.errors.keys())
        self.assertEqual(form.errors['birth_date'], [u'Invalid Birth Date'])


    def test_validate_cpf(self):
        """
        this validation is in a validator of model
        """

        invalid_cpf = '126.131.226-99'

        form = SignUpModelForm({
            'cpf_cnpj': invalid_cpf
        })

        form.is_valid()
        self.assertIn('cpf_cnpj', form.errors.keys())


    def validate_cnpj(self):
        """
        this validation is in a validator of model
        """

        invalid_cnpj = '59.862.754/0001-99'

        form = SignUpModelForm({
            'cpf_cnpj': invalid_cnpj,
        });

        form.is_valid()
        self.assertIn('cpf_cnpj', form.errors.keys())
