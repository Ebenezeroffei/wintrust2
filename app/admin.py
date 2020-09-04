from django.contrib import admin
from .models import Product,Cart,BillingAddress,NewsLetters

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(BillingAddress)
admin.site.register(NewsLetters)
