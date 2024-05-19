from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#for userpersonalinfo
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userpersonalinfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userpersonalinfo.save()
class userpersonalinfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True)
    image_url = models.URLField(max_length=200,blank=True,null=True)
    
    def __str__(self):
        return self.user.username

#for usermedicalinfo
@receiver(post_save, sender=User)
def create_user_medicalprofile(sender, instance, created, **kwargs):
    if created:
        usermedicalinfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_medicalprofile(sender, instance, **kwargs):
    instance.usermedicalinfo.save()  
class usermedicalinfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    allergies=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username

#for userlifestyleinfo
@receiver(post_save, sender=User)
def create_user_lifeprofile(sender, instance, created, **kwargs):
    if created:
        lifestyleinfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_lifeprofile(sender, instance, **kwargs):
    instance.lifestyleinfo.save()
class lifestyleinfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.user.username       

class otp_verification(models.Model):
    otp=models.IntegerField()
    email=models.EmailField(max_length=255,null=True,blank=True)
    phone_number=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()
    
    def __str__(self):
        return self.email   
