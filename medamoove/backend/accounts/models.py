from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Allergy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Medication(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name    
   
class injuries(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name    
    
class surgeries(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name   
    
class chronic_diseases(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

#for userpersonalinfo
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userpersonalinfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userpersonalinfo.save()
    
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]

BLOOD_GROUP_CHOICES = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')]
class userpersonalinfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=PhoneNumberField(("Phone Number"), unique=True,blank=True, null=True)
    image_url = models.URLField(max_length=200,blank=True,null=True)
    public_id = models.CharField(max_length=200,blank=True,null=True) 
    gender=models.CharField(max_length=255,blank=True,null=True,choices=GENDER_CHOICES)
    dob=models.DateField(blank=True,null=True)
    blood_group=models.CharField(max_length=10,null=True,blank=True,choices=BLOOD_GROUP_CHOICES)
    height=models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    weight=models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
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
    allergies = models.ManyToManyField(Allergy, blank=True)
    current_medication = models.ManyToManyField(Medication, blank=True,related_name='current_medication')
    past_medication = models.ManyToManyField(Medication, blank=True,related_name='past_medication')
    injuries=models.ManyToManyField(injuries, blank=True)
    surgeries=models.ManyToManyField(surgeries, blank=True)
    chronic_diseases=models.ManyToManyField(chronic_diseases, blank=True)
    
    def __str__(self):
        return self.user.username
    
    
class occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name    

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
    smoking=models.BooleanField(blank=True,null=True)
    alcohol=models.BooleanField(blank=True,null=True)
    exercise=models.BooleanField(blank=True,null=True)
    occupation=models.OneToOneField(occupation,on_delete=models.CASCADE,blank=True,null=True)
    
    
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
