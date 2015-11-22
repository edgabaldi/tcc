#coding:utf-8
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm

from core.forms import BaseSearchForm
from account.models import User

YESNO_CHOICES = (
    ('',''),
    ('0', u'NÃO'),
    ('1', u'SIM'),
)


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        max_length=254, 
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Usuário'
        }))

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Senha'
        }))


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
                  'neighborhood', 'state', 'cep','username', 'is_active',
                  'is_staff', 'is_marketing',)


class UserSearchForm(BaseSearchForm):

    username = forms.CharField(max_length=40, label=u'Usuário', required=False)
    cpf_cnpj = forms.CharField(max_length=15, label=u'CPF/CNPJ', required=False)
    is_active = forms.NullBooleanField(widget=forms.Select(
        choices=YESNO_CHOICES),label=u'Está Ativo?', required=False)


    class Meta:
        queryset = User.objects.all().order_by('is_active')


class ActivateUserModelForm(forms.ModelForm):

    observation = forms.CharField(
        label=u'Observação', 
        required=False)

    class Meta:
        model = User
        fields = ('is_active',)

    def send_email_activate(self, user):
        from_email = 'naoresponda@brbid.com'
        msg = "Sua conta está ativa. Você já pode participar dos leilões."
        send_mail(u'Sua conta está ativa!', msg, from_email, [user.email]) 

    def send_email_deactivate(self, user):
        observation = self.cleaned_data.get('observation')
        from_email = 'naoresponda@brbid.com'
        msg = "Seu cadastro foi rejeitado. Motivo: {}".format(observation)
        send_mail('Seu cadastro foi negado :(', msg, from_email, [user.email]) 
