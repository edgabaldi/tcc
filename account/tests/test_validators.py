import datetime

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from account.validators import validate_birth_date

class BirthDateValidatorSimpleTestCase(SimpleTestCase):

    def test_validate_birth_date_must_be_true(self):
        birth_date = datetime.date.today() - datetime.timedelta(20)
        self.assertEqual(None, validate_birth_date(birth_date))

    def test_validate_birth_date_must_be_false(self):
        birth_date = datetime.date.today() - datetime.timedelta(16)

        with self.assertRaises(ValidationError):
            validate_birth_date(birth_date)
