from django import forms

from account.models import User


class SignUpModelForm(forms.ModelForm):

    repeat_password = forms.CharField(max_length=32,
                                      widget=forms.PasswordInput,
                                      label='Repita a Senha')

    accepted_terms = forms.BooleanField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 
                  'cpf_cnpj', 'doc', 'doc_entity', 'address', 'city', 
                  'neighborhood', 'state', 'cep','username', 'password',)
