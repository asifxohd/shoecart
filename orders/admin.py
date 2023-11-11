from django.contrib import admin
from .models import Orders,OrdersItem,CancelledOrderItem
# Register your models here.
admin.site.register(Orders)
admin.site.register(OrdersItem)
admin.site.register(CancelledOrderItem)