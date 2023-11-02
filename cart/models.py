from django.db import models
from admin_home.models import Product,SizeVariant

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey('user_authentication.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart ({self.size_variant.size})"