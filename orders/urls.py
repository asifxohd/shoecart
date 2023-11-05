from django.urls import path
from . import views

urlpatterns = [
    path('order_page/', views.load_order_page, name="order_page"),
    path('order_history/', views.order_history, name="order_history"),
    path('place_order/', views.place_order, name="place_order"),
    path('admin_orders/',views.admin_orders, name="admin_orders"),
    path('view_order_details/<str:id>', views.view_order_details,name="view_order_details"),
    
]