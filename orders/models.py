from django.db import models
from user_profile.models import Address
import uuid
from admin_home.models import SizeVariant
from user_authentication.models import CustomUser


# Create your models here.
class Orders(models.Model):
    order_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_purchase_amount = models.PositiveIntegerField(default=1)
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        return str(uuid.uuid4().hex)[:8]
  
    def __str__(self):
        return f"{self.user}'s order details"

class OrdersItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    updated_time = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ORDER_STATUS_CHOICES = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Cancell request send','Cancell request send')
    )
    status = models.CharField(default='Order confirmed', max_length=255, choices=ORDER_STATUS_CHOICES)
    def total_price(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.quantity} x {self.variant} in order {self.order}-------{self.pk}"
    
class CancelledOrderItem(models.Model):
    order_item = models.ForeignKey(OrdersItem, on_delete=models.CASCADE)
    cancellation_reason = models.TextField()
    cancelled_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelled order item: {self.order_item.variant} in order {self.order_item.order}"