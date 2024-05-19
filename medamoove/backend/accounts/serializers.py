from rest_framework import serializers
from django.contrib.auth.models import User


class tokenserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email')
        
class create_user_serializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    phone_number=serializers.CharField()    
        
        