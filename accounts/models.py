from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import order_processor

class User(AbstractUser): 
    phone = models.CharField(max_length=15, unique=True)
    verified_phone = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    verified_email = models.BooleanField(default=False)
    verify_code = models.IntegerField(null=True, blank=True)
    verify_code_time = models.DateTimeField(null=True, blank=True)
    invite_code = models.CharField(max_length=10, unique=True)
    introducer = models.ForeignKey('user', null=True, blank=True,related_name='invited_set' , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles', default='profiles/default-user.jpg') 
    first_name = None
    last_name = None
    name = models.CharField(max_length=30 ,default='')
    shamsi_joined_date = models.CharField(max_length=11, null=True)



class contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    description = models.TextField()