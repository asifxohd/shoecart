from django.db import models
from user_authentication.models import CustomUser

class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    transaction_details = models.CharField(max_length=455)  
    transaction_type = models.CharField(max_length=50) 
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.transaction_details}'
