from django.contrib import admin
from models import ProductPurchased

# Register your models here.
class library(admin.ModelAdmin):
    readonly_fields = ('dateOfPurchase')
    admin.site.register(ProductPurchased)