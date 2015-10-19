# coding: utf-8
from django import forms
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.text import smart_split


class BaseSearchForm(forms.Form):

    STOPWORD_LIST = 'de,o,a,os,as'.split(',')
    DEFAULT_OPERATOR = Q.__and__

    q = forms.CharField(required=False)

    def clean_q(self):
        return self.cleaned_data['q'].strip()

    order_by = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        abstract = True
        base_qs = None
        search_fields = None
        fulltext_indexes = None

    def __init__(self, *args, **kwargs):
        super(BaseSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget.attrs = {'placeholder': self.get_q_placeholder()}

    def get_advanced_search_fields(self):
        return [field for idx, field in enumerate(self) if idx not in (0, 1)]

    def get_q_placeholder(self):
        return ''

    def construct_search(self, field_name, first):
        if field_name.startswith('^'):
            if first:
                return "%s__istartswith" % field_name[1:]
            else:
                return "%s__icontains" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__icontains" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def get_text_query_bits(self, query_string):
        """filter stopwords but only if there are useful words"""

        split_q = list(smart_split(query_string))
        filtered_q = []

        for bit in split_q:
            if bit not in self.STOPWORD_LIST:
                filtered_q.append(bit)

        if len(filtered_q):
            return filtered_q
        else:
            return split_q

    def get_text_search_query(self, query_string):
        filters = []
        first = True

        for bit in self.get_text_query_bits(query_string):

            or_queries = [Q(**{self.construct_search(str(field_name), first): bit}) 
                          for field_name in self.Meta.search_fields]

            filters.append(reduce(Q.__or__, or_queries))
            first = False

        if len(filters):
            return reduce(self.DEFAULT_OPERATOR, filters)
        else:
            return False

    def construct_filter_args(self, cleaned_data):
        args = []

        # if its an instance of Q, append to filter args
        # otherwise assume an exact match lookup
        for field in cleaned_data:

            if hasattr(self, 'prepare_%s' % field):
                q_obj = getattr(self, 'prepare_%s' % field)()
                if q_obj:
                    args.append(q_obj)
            elif isinstance(cleaned_data[field], Q):
                args.append(cleaned_data[field])
            elif field == 'order_by':
                pass  # special case - ordering handled in get_result_queryset
            elif cleaned_data[field]:
                if isinstance(cleaned_data[field], list) or isinstance(cleaned_data[field], QuerySet):
                    args.append(Q(**{field + '__in': cleaned_data[field]}))
                else:
                    args.append(Q(**{field: cleaned_data[field]}))

        return args

    def get_order_by(self):
        return self.cleaned_data['order_by'].split(',')

    def get_result_queryset(self):
        qs = self.Meta.base_qs

        cleaned_data = self.cleaned_data.copy()
        query_text = cleaned_data.pop('q', None)

        qs = qs.filter(*self.construct_filter_args(cleaned_data))

        if query_text:
            # construct text search for sqlite, or for when no fulltext indexes are defined
            text_q = self.get_text_search_query(query_text)
            if text_q:
                qs = qs.filter(text_q)
            else:
                qs = qs.none()

        if self.cleaned_data['order_by']:
            qs = qs.order_by(*self.get_order_by())

        return qs

    def get_result_queryset_by_user(self, user):
        return self.get_result_queryset().by_user(user)