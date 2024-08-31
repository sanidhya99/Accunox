from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import *
class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    about=models.CharField(max_length=100)
    pic=models.CharField(max_length=2000,default="https://iili.io/HN6dJmF.png")
    friends = models.ManyToManyField('self', symmetrical=True, related_name='friends_with')
    
    objects=UserManager()
    
    REQUIRED_FIELDS=['name']

    USERNAME_FIELD='email'