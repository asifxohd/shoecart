from django.urls import path
from . import views

urlpatterns = [ 
    path('admin_dashboard', views.admin_dash, name='admin_dashboard'),
    path('sales', views.admin_sales, name="sales_report"),
    path('sales_report_filter', views.filter_by_date_sales_report, name="sales_report_filter"),
    path('datefilter_dashboard/', views.datefilter_dashboard, name="datefilter_dashboard"),

]
