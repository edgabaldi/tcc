import datetime

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from account.validators import validate_birth_date, validate_cpf_cnpj

class BirthDateValidatorSimpleTestCase(SimpleTestCase):

    def test_validate_birth_date_must_be_true(self):
        valid_year = datetime.date.today().year - 20
        birth_date = datetime.date.today().replace(year=valid_year)
        self.assertEqual(None, validate_birth_date(birth_date))

    def test_validate_birth_date_must_be_false(self):
        invalid_year = datetime.date.today().year - 16
        birth_date = datetime.date.today().replace(year=invalid_year)

        with self.assertRaises(ValidationError):
            validate_birth_date(birth_date)


class CPFValidatorSimpleTestCase(SimpleTestCase):

    def setUp(self):
        self.valid_cpf = '126.131.226-09'
        self.invalid_cpf = '126.131.226-99'
        self.valid_cnpj = '59.862.754/0001-01'
        self.invalid_cnpj = '59.862.754/0001-99'

    def test_validate_cpf_should_return_None(self):
        self.assertEqual(None, validate_cpf_cnpj(self.valid_cpf))

    def test_validate_cpf_should_raise_validation_error(self):
        with self.assertRaises(ValidationError):
            validate_cpf_cnpj(self.invalid_cpf)

    def test_validate_cnpj_should_return_none(self):
        self.assertEqual(None, validate_cpf_cnpj(self.valid_cnpj))

    def test_validate_cnpj_should_raise_validation_error(self):
        with self.assertRaises(ValidationError):
            validate_cpf_cnpj(self.invalid_cnpj)
