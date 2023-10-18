from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.landing, name='homepage'),
    path('baseuser/', views.baseuser, name='baseuser'),
    path('product/', views.product_page, name='product_page'),
    path('about/', views.about, name='about'),
    path('shoes/', views.shoes, name='shoes'),
    path('contact/', views.contact, name='contact'),
    path('product_details', views.product_details, name="product_details"),
    
   ]