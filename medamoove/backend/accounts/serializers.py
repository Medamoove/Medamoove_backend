from rest_framework import serializers
from django.contrib.auth.models import User


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
    