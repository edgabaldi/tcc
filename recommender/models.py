from django.db import models


class ProductSimilarity(models.Model):

    product = models.ForeignKey('product.Product')
    is_similar_to = models.ForeignKey('product.Product', related_name='similars')
    score = models.DecimalField(decimal_places=5, max_digits=6)

    def __unicode__(self):
        return u'Product: {} Similar To: {} Score: {}'.format(
            self.product, self.is_similar_to, self.score)
