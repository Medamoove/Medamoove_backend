from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class tokenserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email')
        
class create_user_serializer(serializers.Serializer):
    username=serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True) 
        
class google_profile(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    profile_pic=serializers.URLField(required=False, allow_blank=True, allow_null=True)     
    
class login_serializer(serializers.Serializer):
    email=serializers.EmailField(required=False, allow_blank=True, allow_null=True)   
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    

class otp_serializer(serializers.Serializer):
    otp=serializers.IntegerField()
    email=serializers.EmailField(required=False, allow_blank=True, allow_null=True)   
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    username=serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
#serializers for userpersonalinfo        
class userpersonalinfo_serializer(serializers.ModelSerializer):
    class Meta:
        model=userpersonalinfo
        fields='__all__'
        
#serializers for usermedicalinfo
class usermedicalinfo_serializer(serializers.ModelSerializer):
    class Meta:
        model=usermedicalinfo
        fields='__all__'    
    
#serializers for lifestyleinfo        
class lifestyleinfo_serializer(serializers.ModelSerializer):
    class Meta:
        model=lifestyleinfo
        fields='__all__'       
        
#serializers for allergies,medications,injuries,surgeries,chronic_diseases,occupation        

class allergies_serializer(serializers.ModelSerializer):
    class Meta:
        model=Allergy
        fields='__all__'
        
class medication_serializer(serializers.ModelSerializer):
    class Meta:
        model=Medication
        fields='__all__'        
       
class injuries_serializer(serializers.ModelSerializer):
    class Meta:
        model=injuries
        fields='__all__'           
        
class surgeries_serializer(serializers.ModelSerializer):
    class Meta:
        model=surgeries
        fields='__all__'        
   
class chronic_diseases_serializer(serializers.ModelSerializer):
    class Meta:
        model=chronic_diseases
        fields='__all__'        
        
class occupation_serializer(serializers.ModelSerializer):
    class Meta:
        model=occupation
        fields='__all__'        
        
        
#update serializers for userpersonalinfo        

class update_userpersonalinfo_serializer(serializers.ModelSerializer): 
    class Meta:
        model=userpersonalinfo
        fields=['phone_number','gender','dob','blood_group','height','weight']
        
        
# wallet serializers               

class files_serializer(serializers.ModelSerializer):
    class Meta:
        model=files
        fields=['file_url','public_id']        
        
class card_serializer(serializers.ModelSerializer):
    class Meta:
        model=card
        fields=['type','tags','description','date','created_for']  
        
class getcard_serializer(serializers.ModelSerializer):
    class Meta:
        model=card
        fields='__all__'       
        
class getfiles_serializer(serializers.ModelSerializer):
    class Meta:
        model=files
        fields=['file_url']               