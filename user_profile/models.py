from django.db import models
from user_authentication.models import CustomUser
# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    address_line = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    landmark = models.TextField()
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Address"

