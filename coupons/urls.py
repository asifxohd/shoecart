from django.urls import path
from . import views

urlpatterns = [
   path('coupons', views.render_coupons,name="coupons_page"),
   path('add_coupons', views.add_coupons,name="add_coupons"),
   path('edit_coupons/<str:id>', views.edit_coupons,name="edit_coupons"),
   path('delete_coupons/<str:id>', views.delete_coupons,name="delete_coupons"),
   path('apply_coupon', views.apply_coupon,name="apply_coupon"),
   path('remove_coupon', views.remove_coupon,name="remove_coupon"),
]