from django.db import models
from django.utils import timezone
from user_authentication.models import CustomUser
from django.db.models import Q

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(admin=user)
        qs = self.get_queryset().filter(lookup).distinct()

class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='first_person_threads')
    admin =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_threads')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['first_person', 'admin']
        
    objects = ThreadManager()
        
        
class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name="chatmessage_thread")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
