from django.urls import path
from .import views

urlpatterns = [
    
    path('admin_base', views.admin_base, name='admin_base'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_products', views.admin_products, name='admin_products'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('admin_catogeory', views.admin_catogory, name="admin_catogeory"),
    path('user_status/<str:id>', views.user_status, name='user_status'),
    path('add_products', views.add_products, name="add_products"),
    path('category_status/<str:id>', views.category_status, name='category_status'),
    path('edit_category/<str:id>', views.edit_category, name='edit_category'),
    path('add_category', views.add_category, name="add_category"),
    path('product_varient/<str:id>', views.show_product_varient, name='product_varient'),
    path('admin_trash/product_varient/<str:id>', views.trash_product_varient, name='trash_product_varient'),
    path('admin_trash/', views.admin_trash, name='admin_trash'),
    path('soft_delete_product/<str:id>/', views.ajax_soft_delete_product, name='soft_delete_product'),
    path('restore_product/<str:id>/', views.restore_product, name='restore_product'),
    path('edit_product/<str:id>/', views.edit_product, name='edit_product'),
    path('add_variand/<str:id>/', views.add_variand, name="add_variand"),
    path('edit_variand/<str:id>/', views.edit_variand, name="edit_variand"),
    path('banner', views.admin_banner, name="banner_page"),
    path('add_banner', views.add_banner, name="add_banner"),
    path('edit_banner/<str:id>/', views.admin_edit_banner, name="edit_banner"),
    path('delete_banner/<str:id>/', views.delete_banner, name="delete_banner"),
    ]
    
    