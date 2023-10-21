from django.contrib import admin
from .models import Product, SizeVariant, Category,ProductImage

# Register your models here.
admin.site.register(Product)
admin.site.register(SizeVariant)
admin.site.register(Category)
admin.site.register(ProductImage)

