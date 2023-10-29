from django.urls import path
from . import views

urlpatterns = [
    
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_user_profile', views.update_user_profile, name="update_user_profile"),
    path('change_password/', views.change_password, name="change_password"),
]