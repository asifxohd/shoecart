from django.urls import path
from . import views

urlpatterns = [ 
    path('cart_page/', views.cart_page, name='cart_page'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_item_from_cart/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('update_cart', views.update_cart, name="update_cart"),
]
