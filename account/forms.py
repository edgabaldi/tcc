#coding:utf-8
from django import forms

from core.forms import BaseSearchForm
from account.models import User

YESNO_CHOICES = (
    ('',''),
    ('0', u'NÃO'),
    ('1', u'SIM'),
)


class SignUpModelForm(forms.ModelForm):
    """
    ModelForm that allow create users in website
    """

    repeat_password = forms.CharField(max_length=32,
                                      widget=forms.PasswordInput,
                                      label='Repita a Senha')

    accepted_terms = forms.BooleanField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 
                  'cpf_cnpj', 'doc', 'doc_entity', 'address', 'city', 
                  'neighborhood', 'state', 'cep','username','password',)
        widgets = {
            'password': forms.PasswordInput,
        }


class UserModelForm(forms.ModelForm):
    """
    ModelForm that allow create and update users in backend
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 
                  'cpf_cnpj', 'doc', 'doc_entity', 'address', 'city', 
                  'neighborhood', 'state', 'cep','username', 'is_active',)


class UserSearchForm(BaseSearchForm):

    username = forms.CharField(max_length=40, label=u'Usuário', required=False)
    cpf_cnpj = forms.CharField(max_length=15, label=u'CPF/CNPJ', required=False)
    is_active = forms.BooleanField(widget=forms.Select(
        choices=YESNO_CHOICES),label=u'Está Ativo?', required=False)


    class Meta:
        queryset = User.objects 
