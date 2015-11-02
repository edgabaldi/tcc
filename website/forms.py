#coding:utf-8
from django import forms

from product.models import Bid


class BidModelForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('user', 'product', 'value',)

    def clean(self):
        cleaned = super(BidModelForm, self).clean()

        product = cleaned.get('product')
        value = cleaned.get('value')

        if value > self._max_value_of(product):
            raise forms.ValidationError(u"Lance Inválido: Valor máximo do "
                                        "lance ultrapassado.")

        if value < self._min_value_of(product):
            raise forms.ValidationError(u"Lance Inválido: Valor deve ser maior"
                                        "que o valor atual")

        return cleaned

    def _max_value_of(self, product):
        value = self._get_last_value_of(product)
        return value * 10

    def _min_value_of(self, product):
        value = self._get_last_value_of(product)
        return value + 1

    def _get_last_value_of(self, product):

        bid_list = product.bids.order_by('-created_at')
        if len(bid_list) > 0:
            bid = bid_list[0]
            return bid.value
        return product.initial_price
