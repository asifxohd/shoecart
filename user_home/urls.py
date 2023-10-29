from django.urls import path
from . import views

urlpatterns = [
    
    path('homepage', views.homepage, name='homepage'),
    path('baseuser/', views.baseuser, name='baseuser'),
    path('product/', views.product_page, name='product_page'),
    path('about/', views.about, name='about'),
    path('shoes/', views.shoes, name='shoes'),
    path('contact/', views.contact, name='contact'),
    path('product_details/<str:id>', views.product_details, name="product_details"),
    path('products_men', views.products_men, name="products_men"),
    path('products_women', views.products_women, name="products_women"),
    path('unisex_products', views.unisex, name='unisex_products'),
    path('show_catogery/<int:id>', views.show_category, name='show_catogery'),
    path('show_price_filtering', views.show_price_filtering, name='show_price_filtering'),
    path('show_price_between', views.show_price_between, name='show_price_between'),
    path('autocompleat', views.autocompleat, name='autocompleat'),

    ]