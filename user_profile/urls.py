from django.urls import path
from . import views

urlpatterns = [
    
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_user_profile', views.update_user_profile, name="update_user_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('address_page', views.address_page, name="address_page"),
    path('add_address/', views.add_address, name="add_address"),
    path('update_address/<str:id>/', views.update_address, name="update_address"),
    path('delete_address/<str:id>/',views.delete_address, name="delete_address"),
    
]