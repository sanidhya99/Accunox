from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import *
class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=50)
    age=models.PositiveIntegerField(null=True,blank=True)
    gender=models.CharField(max_length=10,null=True,blank=True)
    about=models.CharField(max_length=100,null=True,blank=True)
    pic=models.CharField(max_length=2000,default="https://iili.io/HN6dJmF.png",null=True,blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, related_name='friends_with', blank=True)
    objects=UserManager()
    
    REQUIRED_FIELDS=['name']

    USERNAME_FIELD='email'