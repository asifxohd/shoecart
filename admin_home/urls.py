from django.urls import path
from . import views

urlpatterns = [
    
    path('admin_base', views.admin_base, name='admin_base'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_dashboard', views.admin_dash, name='admin_dashboard'),
    path('admin_products', views.admin_products, name='admin_products'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('admin_catogeory', views.admin_catogory, name="admin_catogeory"),
    path('user_status/<str:id>', views.user_status, name='user_status'),
    path('add_products', views.add_products, name="add_products"),
    path('category_status/<str:id>', views.category_status, name='category_status'),
    path('edit_category/<str:id>', views.edit_category, name='edit_category'),
    path('add_category', views.add_category, name="add_category")
    
    ]