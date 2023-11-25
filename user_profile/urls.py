from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_user_profile', views.update_user_profile, name="update_user_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('address_page', views.address_page, name="address_page"),
    path('add_address/', views.add_address, name="add_address"),
    path('update_address/<str:id>/', views.update_address, name="update_address"),
    path('delete_address/<str:id>/',views.delete_address, name="delete_address"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_side/forgot_password.html'), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='user_side/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_side/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_side/password_reset_complete.html'), name="password_reset_complete"),
   
    ]                           