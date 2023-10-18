from django.urls import path
from . import views

urlpatterns = [
    path('admin_base', views.admin_base, name='admin_base'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_dashboard', views.admin_dash, name='admin_dashboard'),
    path('admin_products', views.admin_products, name='admin_products'),
    path('admin_users', views.admin_users, name='admin_users'),
]