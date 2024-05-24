from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class doctor_serializer(serializers.ModelSerializer):
    class Meta:
        model=doctors
        fields=['first_name','last_name','email','PhoneNumber']
        
class patient_serializer(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields=['first_name','last_name','email','PhoneNumber']        
        
        
        
class retrivedoctor_serializer(serializers.ModelSerializer):
    class Meta:
        model=doctors
        fields=['docid','first_name','last_name','email','PhoneNumber']
        
class retrivepatient_serializer(serializers.ModelSerializer):
    class Meta:
        model=patient
        fields=['pid','first_name','last_name','email','PhoneNumber'] 
        
