from django.urls import path
from . import views

urlpatterns = [ 
    path('cart_page/', views.cart_page, name='cart_page'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_item_from_cart/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('update_cart', views.update_cart, name="update_cart"),
    path('checkout_address', views.checkout_address,name="checkout_address"),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_add_address/', views.checkout_add_address, name='checkout_add_address'),
    path('checkout_update_address/<int:id>/', views.checkout_update_address, name='checkout_update_address'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_to_wishlist',views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/',views.remove_wishlist, name='remove_wishlist'),
]
