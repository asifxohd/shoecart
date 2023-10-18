from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('otp', views.otp, name='otppage'),  
    path('send_otp/', views.send_6_digit_otp_email, name='send_otp'),
]