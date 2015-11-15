#coding:utf-8
from django import forms
from django.contrib.auth import get_user_model

from core.forms import BaseSearchForm
from recommender.models import UserSimilarity

User = get_user_model()


class UserSimilaritySearchForm(BaseSearchForm):

    user = forms.ModelChoiceField(
        queryset = User.objects.filter(is_active=True),
        required=False,
        empty_label=None,
        label=u'Usuário')

    class Meta:
        queryset = UserSimilarity.objects.select_related(
            'user','product', 'product__model', 
            'product__model__brand',)
