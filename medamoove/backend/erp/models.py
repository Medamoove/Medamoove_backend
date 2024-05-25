from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from accounts.models import *


class doctors(models.Model):
    docid=models.AutoField(primary_key=True)
    hid=models.ForeignKey('accounts.hospitals',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True,null=True,blank=True)
    PhoneNumber=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by',blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',blank=True,null=True)
    
    def __str__(self):
        return self.first_name+" "+self.last_name
    
class patient(models.Model):
    pid=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    hid=models.ForeignKey('accounts.hospitals',on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator')
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True,null=True,blank=True)
    PhoneNumber=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True)
    
    def __str__(self):
        return self.user.username    