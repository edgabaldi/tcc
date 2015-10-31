from django import forms
from django.db.models import Q, Model


class BaseSearchForm(forms.Form):

    class Meta:
        abstract = True
        queryset = None

    def get_result_queryset(self):

        qs = self.Meta.queryset
        cleaned_data = self.cleaned_data.copy()
        qs = qs.filter(*self._contruct_filter_args(cleaned_data))

        return qs

    def _contruct_filter_args(self, cleaned_data):

        args = []
        
        for key, value in cleaned_data.items():

            if self._is_boolean(value) or self._is_model_object(value):
                args.append(Q(**{key:value}))

            if self._is_string(value):
                args.append(Q(**{
                    '%s__icontains' % key : value}))
        return args

    def _is_boolean(self, value):
        return isinstance(value, bool)

    def _is_model_object(self, value):
        return isinstance(value, Model)

    def _is_string(self, value):
        return isinstance(value, str) or isinstance(value, unicode)

