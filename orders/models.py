from django.db import models
from user_profile.models import Address
import uuid
from admin_home.models import SizeVariant
from user_authentication.models import CustomUser


# Create your models here.
class Orders(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField()    
    def __str__(self):
        return f"{self.user}'s order details"

class OrdersItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ORDER_STATUS_CHOICES = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(default='Order confirmed', max_length=20, choices=ORDER_STATUS_CHOICES)
    def total_price(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.quantity} x {self.variant} in order {self.order}-------{self.pk}"