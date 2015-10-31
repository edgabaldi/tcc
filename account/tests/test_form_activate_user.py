#coding: utf-8
from django.test import TestCase
from django.core import mail
from django.conf import settings

from account.forms import ActivateUserModelForm

from model_mommy import mommy


class ActivateUserModelFormTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(
            settings.AUTH_USER_MODEL,
            email='foo@bar.com',
            is_active=False)

    def test_send_email_activate(self):
        form = ActivateUserModelForm({
            'is_active': True,
        })
        form.is_valid()
        form.send_email_activate(self.user)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject, u'Sua conta está ativa!')

    def test_send_email_deactivate(self):
        form = ActivateUserModelForm({
            'is_active': False,
            'observation': 'denied'
        })
        form.is_valid()
        form.send_email_deactivate(self.user)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject, u'Seu cadastro foi negado :(')
