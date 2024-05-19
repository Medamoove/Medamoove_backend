from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
class userpersonalinfo(User,models.Model):
    phone_number=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True)
    

class otp_verification(models.Model):
    otp=models.IntegerField()
    email=models.EmailField(max_length=255,null=True,blank=True)
    phone_number=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    
    def __str__(self):
        return self.email   
