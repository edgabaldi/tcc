from copy import copy
import datetime
import pickle

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from product.models import Product, Brand, Model, Bid

User = get_user_model()

now = datetime.datetime(2015, 10, 16, 12 ,00)


class Command(BaseCommand):

    def _bid_kwargs(self, product, user, bid_dict):

        date = bid_dict['created_at']
        date = date.replace(tzinfo=None)
        
        return {
            'product': product,
            'user': user,
            'value': bid_dict['value'],
            'created_at': date,
        }

    def _user_kwargs(self, bid_dict):

        bid_dict = copy(bid_dict)

        del bid_dict['value']
        del bid_dict['created_at']

        if bid_dict['birth_date'] is None:
            bid_dict['birth_date'] =  now.date().replace(year=1986)

        return bid_dict

    def _vehicle_kwargs(self, each_dict):

        each_dict = copy(each_dict)

        brand, created = Brand.objects.get_or_create(
            name=each_dict['brand_name'],
            is_active=True)

        model, created = Model.objects.get_or_create(
            brand=brand,
            name=each_dict['model_name'],
            is_active=True)

        for key in ['photos', 'bids', 'brand_name', 'model_name']:
            del each_dict[key]

        extra = {
            'model': model,
            'description' : 'xxx',
            'clock_starts_at': now,
            'status': 'em_loteamento'
        }

        each_dict.update(extra)

        return each_dict

    def handle(self, *args, **options):

        with open('tmp/data/data.pkl') as file:

            self.data = pickle.load(file)

        for each in self.data:

            vehicle_dict = self._vehicle_kwargs(each)

            product, created = Product.objects.get_or_create(**vehicle_dict)

            for bid in each.get('bids'):
                user_dict = self._user_kwargs(bid)
                user, created = User.objects.get_or_create(**user_dict)

                bid_dict = self._bid_kwargs(product, user, bid)
                Bid.objects.get_or_create(**bid_dict)

