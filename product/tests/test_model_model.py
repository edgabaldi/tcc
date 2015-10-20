#coding:utf-8
from django.test import TestCase

from model_mommy import mommy

class ModelTestCase(TestCase):

    def test_unicode(self):

       self.obj = mommy.prepare('product.Model',
                      brand__name='Foo',
                      name=u'Bár',
                      is_active=True)

       self.assertEqual(u'Foo - Bár', self.obj.__unicode__())

