import datetime

from django.test import SimpleTestCase

from account.forms import SignUpModelForm


class SignUpModelFormTestCase(SimpleTestCase):

    def test_validate_birth_date(self):
        """
        this validation is in a validator of model.
        """

        invalid_birth_date = datetime.date.today() - datetime.timedelta(16)

        form = SignUpModelForm({
            'birth_date': invalid_birth_date
        })

        form.is_valid()

        self.assertIn('birth_date', form.errors.keys())
        self.assertEqual(form.errors['birth_date'], [u'Invalid Birth Date'])
