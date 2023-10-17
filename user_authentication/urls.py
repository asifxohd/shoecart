from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('otp', views.otp, name='otppage'),  
    path('landing', views.landing, name='landing'),
    path('send_otp/', views.send_6_digit_otp_email, name='send_otp'),
]