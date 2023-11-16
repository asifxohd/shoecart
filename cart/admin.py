from django.contrib import admin
from .models import CartItem,Wishlist

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Wishlist)