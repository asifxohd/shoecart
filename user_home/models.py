from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

# Create your models here.
class Contact(models.Model):
    email = models.CharField(max_length=250)
    message = models.TextField()
    
@receiver(post_save, sender=Contact)
def _post_save_receiver(sender, instance, **kwargs):
    subject = 'Your 6-digit OTP for email verification'
    message = f'{instance.message}'
    from_email = 'shoecartcalicut@gmail.com'
    recipient_email = instance.email  
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
