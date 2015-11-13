from django.db import models


class ProductSimilarity(models.Model):
    reference = models.CharField(max_length=150)
    similar = models.ForeignKey('product.Product', related_name='similars')
    score = models.DecimalField(decimal_places=5, max_digits=6)

    def __unicode__(self):
        return u'Product: {} Similar To: {} Score: {}'.format(
            self.reference, self.similar, self.score)
