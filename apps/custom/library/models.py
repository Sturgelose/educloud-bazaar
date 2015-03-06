from django.db import models
from oscar.core.loading import get_model
from django.contrib.auth import get_user_model
from django.conf import settings

User = settings.AUTH_USER_MODEL
Product = get_model('catalogue', 'Product')
Basket = get_model('basket', 'Basket')


class ProductPurchased(models.Model):
    owner = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    dateOfPurchase = models.DateTimeField(auto_now_add=True)
    basket = models.ForeignKey(Basket)
    quantity = models.IntegerField(default=1, blank=False)
    validated = models.BooleanField(default=True) #TODO Only in demo phase

    def __str__(self):
        return self.product.title

    @classmethod
    def create(cls):
        obj = cls()
        return obj