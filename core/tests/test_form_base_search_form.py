from unittest import skip

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django import forms

from core.forms import BaseSearchForm

from model_mommy import mommy

User = get_user_model()


class SingleFieldSearchForm(BaseSearchForm):

    class Meta:
        queryset = User.objects

    username = forms.CharField(max_length=32, required=False)


class MultipleFieldSearchForm(BaseSearchForm):

    class Meta:
        queryset = User.objects

    username = forms.CharField(max_length=32, required=False)
    cpf_cnpj = forms.CharField(max_length=15, required=False)


class SetupMixin(object):

    form_class = None

    def get_form_class(self):
        if self.form_class:
            return self.form_class
        raise ImproperlyConfigured("You must define form_class attribute")

    def _setup_users(self):

        self.foobar = mommy.make(
            settings.AUTH_USER_MODEL, 
            username='foobar',
            cpf_cnpj='12345')

        self.baz = mommy.make(
            settings.AUTH_USER_MODEL,
            username='baz',
            cpf_cnpj='67890')

    def _setup_form(self, form_dict):
        form_class = self.get_form_class()
        self._setup_users()
        self.form = form_class(form_dict)
        self.form.is_valid()
        return self.form.get_result_queryset()


class SingleSearchFormTestCase(SetupMixin, TestCase):
    """
    Test a BaseSearchForm with only one search field
    """

    form_class = SingleFieldSearchForm

    def test_get_result_queryset(self):
        form_dict = {'username': 'baz'}
        result = self._setup_form(form_dict)
        self.assertEqual(self.baz, result.get())

    def test_get_result_queryset_icontains(self):
        form_dict = {'username': 'foo'}
        result = self._setup_form(form_dict)
        self.assertEqual(self.foobar, result.get())


class MultipleSearchFormTestCase(SetupMixin, TestCase):
    """
    Test a BaseSearchForm with more that one search field
    """

    form_class = MultipleFieldSearchForm

    def test_get_result_queryset(self):
        form_dict = {'username': 'baz', 'cpf_cnpj': '67890'}
        result = self._setup_form(form_dict)
        self.assertEqual(self.baz, result.get())

    def test_get_result_queryset_icontains(self):
        form_dict = {'username': 'foo', 'cpf_cnpj': '12345'}
        result = self._setup_form(form_dict)
        self.assertEqual(self.foobar, result.get())

