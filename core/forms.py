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

        for field in cleaned_data:

            if cleaned_data[field]:

                if isinstance(cleaned_data[field], Model):
                    args.append(Q(**{field: cleaned_data[field]}))
                else:
                    args.append(Q(**{
                        '%s__icontains' % field : cleaned_data[field]}))

        return args

