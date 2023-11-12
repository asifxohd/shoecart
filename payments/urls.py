from django.urls import path
from . import views

urlpatterns = [
   path('wallet_page', views.wallet_page, name="wallet_page"),
   path('collect_payment_details/', views.collect_payment_details, name="collect_payment_details"),
   path('verify_wallet_payment/', views.verify_wallet_payment, name="verify_wallet_paymen")
]