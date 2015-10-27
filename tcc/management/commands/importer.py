#coding:utf-8
from decimal import Decimal
from copy import copy
import datetime
import pickle
import pprint

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from product.models import Product, Brand, Model, Bid

User = get_user_model()

now = datetime.datetime(2015, 10, 16, 12 ,00)


class Command(BaseCommand):

    photo_list = []

    def _vehicle_kwargs(self, each_dict):

        each_dict = copy(each_dict)

        brand, created = Brand.objects.get_or_create(
            name=each_dict['brand_name'],
            is_active=True)

        model, created = Model.objects.get_or_create(
            brand=brand,
            name=each_dict['model_name'],
            is_active=True)

        for key in ['veiculo_id', 'photos', 'bids', 'brand_name', 'model_name']:
            del each_dict[key]

        extra = {
            'model': model,
            'clock_starts_at': now,
        }

        if each_dict.get('initial_price') is None:

            extra.update({
                'initial_price': Decimal('0'),
            })

        each_dict.update(extra)

        return each_dict

    def _bid_kwargs(self, product, user, bid_dict):

        date = bid_dict['created_at']
        date = date.replace(tzinfo=None)
        
        return {
            'product': product,
            'user': user,
            'value': bid_dict['value'] or Decimal('0'),
            'created_at': date,
        }

    def _user_kwargs(self, user_dict):

        user_dict = copy(user_dict)

        if user_dict['birth_date'] is None:
            user_dict['birth_date'] =  now.date().replace(year=1986)

        return user_dict

    def _save_photos_to_download(self, id, photo):
        path_list = photo.split('/')
        url ="https://brbid-assets-prod.s3.amazonaws.com/media/fotos/" + path_list[-1]

        self.photo_list.append({
            'id': id, 
            'url': url,
        })

    def handle(self, *args, **options):
        """
         salvar pk do veiculo e endereço de download.
        """

        with open('data.pkl') as file:

            self.data = pickle.load(file)

        for each in self.data:
            vehicle_dict = self._vehicle_kwargs(each)
            product, created = Product.objects.get_or_create(**vehicle_dict)

            for photo in each.get('photos'):
                self._save_photos_to_download(product.pk, photo)

            bid_list = []
            for bid in each.get('bids'):

                try:

                    user = bid.get('user')
                    user_dict = self._user_kwargs(user)
                    user, created = User.objects.get_or_create(**user_dict)

                    bid_kwargs = self._bid_kwargs(product, user, bid)
                    bid_list.append(Bid(**bid_kwargs))
                except Exception, e:
                    print user, str(e)

            Bid.objects.bulk_create(bid_list)

        with open('photos.pkl', 'w') as arquivo:
            pickle.dump(self.photo_list, arquivo)
