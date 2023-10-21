from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    # Your existing fields
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    date_of_join = models.DateField(default=timezone.now, null=True, blank=True)
   

    def __str__(self):
        return self.first_name
