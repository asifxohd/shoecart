from django.db import models
from user_authentication.models import CustomUser

# Create your models here.
class Coupons(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    ]
    coupon_code = models.CharField(max_length=20, unique=True, default=None)
    coupon_title = models.CharField(max_length=250, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage',
        null=True,
        blank=True
    )
    valid_from = models.DateField()
    valid_to = models.DateField(null=True)
    limit = models.PositiveIntegerField(null=True)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'CODE: {self.coupon_code} - NAME :- {self.coupon_title}'
    

class CouponUsage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} used {self.coupon.coupon_code} on {self.used_at}'