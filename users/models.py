from django.db import models
from authentication.models import CustomUser
# Create your models here.
class Request(models.Model):
    subject=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='request_reciever')
    sender=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='request_sender')
    accept=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line
    def __str__(self):
        return self.sender
    
    