from django.urls import path
from . import views

urlpatterns = [ 
    path('cart_page/', views.cart_page, name='cart_page'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
]
