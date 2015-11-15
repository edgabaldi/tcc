from django.db import models

from django.conf import settings


class ProductSimilarity(models.Model):

    reference = models.CharField(max_length=150)
    similar = models.ForeignKey('product.Product', related_name='similars')
    score = models.DecimalField(decimal_places=5, max_digits=6)

    def __unicode__(self):
        return u'Product: {} Similar To: {} Score: {}'.format(
            self.reference, self.similar, self.score)


class UserSimilarity(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey('product.Product')
    score = models.DecimalField(decimal_places=5, max_digits=6)

    def __unicode__(self):
        return u'User: {} should like: {} Score: {}'.format(
            self.user, self.product, self.score)
