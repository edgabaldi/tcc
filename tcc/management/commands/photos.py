import os
import pickle
import requests
from StringIO import StringIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from product.models import Product, Photo

PHOTO_DIR = 'media/photos/'

class Command(BaseCommand):

    def _download(self, url):
        response = requests.get(url)
        file = StringIO(response.content)
        file_content = ContentFile(file.read())
        return file_content

    def _get_filename(self, url):
        return url.split('/')[-1]

    def _get_product(self, id):
        return Product.objects.get(id=id)
 
    def handle(self, *args, **options):


        with open('photos.pkl') as file:

            self.data = pickle.load(file)

        for each in self.data:

            id = each.get('id')
            url = each.get('url')

            product = self._get_product(id)
            filename = self._get_filename(url)

        
            photo = Photo(product=product)

            if filename in os.listdir(PHOTO_DIR):
                photo_path = '/'.join(['photos', filename])
                photo.file = photo_path
            else:
                file_content = self._download(url)
                photo.file.save(filename, file_content)

            photo.save()
