from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


from django.shortcuts import redirect
""" from allauth.socialaccount.models import SocialAccount """

from .tests import *
from django.utils import timezone
import threading
from .models import *

class CustomAuthTokenView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        
        if not username or not email:
            return Response({"error": "Username and email are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            return Response({"error": "Invalid username or email."}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email,
            'id': user.id
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
def google_login(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    user = request.user
    refresh = RefreshToken.for_user(user)

    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    # Redirect or render a template with the token
    return JsonResponse(token)  


class create_user(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=create_user_serializer(data=data)
            if serializer.is_valid():
                username=serializer.data.get('username')
                email=serializer.data.get('email')
                phone_number=serializer.data.get('phone_number')
                print(username,email,phone_number)
                if email and User.objects.filter(email=email).exists():
                    return Response({"error": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)  
                elif email:
                    
                    email_sent,error_msg=send_otp_email(email,otp)
                    if error_msg:
                        return Response({"error": "otp not sent"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    expiry_time = timezone.now() + timezone.timedelta(seconds=30)
                    otp_instance = otp_verification.objects.filter(email=email).first()
                    #checking if already otp is present for the email
                    if otp_instance:
                        otp_instance.delete()
                        otp_verification.objects.create(email=email,otp=otp,expires_at=expiry_time)
                    else:
                        otp_verification.objects.create(email=email,otp=otp,expires_at=expiry_time)
                            
                    request.session['user_details'] = serializer.validated_data
                    
                    # Start a thread to delete OTP after expiry time
                    t = threading.Thread(target=delete_expired_otp, args=(email,))
                    t.start()
                    data={
                        "username":username,
                        "email":email,
                        "phone_number":phone_number
                    }
                    return JsonResponse({'message':'otp sent to mail successfully',"data":data},status=status.HTTP_200_OK) 
                
                elif phone_number and User.objects.filter(phone_number=phone_number).exists():
                    return Response({"error": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)
                
                elif phone_number:
                    phone_number_sent,error_msg=send_otp_email(phone_number,otp)
                    if error_msg:
                        return JsonResponse({'messages':error_msg},status=status.HTTP_400_BAD_REQUEST)
                    expiry_time = timezone.now() + timezone.timedelta(seconds=30)
                    
                    otp_instance = otp_verification.objects.filter(phone_number=phone_number).first()
                    #checking if already otp is present for the email
                    if otp_instance:
                        otp_instance.delete()
                        otp_verification.objects.create(phone_number=phone_number,otp=otp,expires_at=expiry_time)
                    else:
                        otp_verification.objects.create(phone_number=phone_number,otp=otp,expires_at=expiry_time)    
                    request.session['user_details'] = serializer.validated_data
                    
                    t = threading.Thread(target=delete_expired_otp, args=(phone_number,))
                    t.start()
                    data={
                        "username":username,
                        "email":email,
                        "phone_number":phone_number
                    }
                    return JsonResponse({'message':'otp sent successfully to phone number',"data":data},status=status.HTTP_200_OK)
                
                else:
                    return Response({"error": "email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
                    
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)     
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


import time
def delete_expired_otp(email):
    # Sleep for 30 seconds
    time.sleep(120)

    # Delete expired OTP instances for the email
    otp_verification.objects.filter(email=email, expires_at__lte=timezone.now()).delete()
    
    
class otp_verification_signin(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=otp_serializer(data=data)
            if serializers.is_valid():
                otp=serializers.data.get('otp')
                email=serializers.data.get('email')
                phone_number=serializers.data.get('phone_number')
                username=serializers.data.get('username')
                if not otp:
                    return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                if email and otp_verification.objects.filter(email=email,otp=otp,expires_at__gte=timezone.now()).first():
                    user=User.objects.create_user(username=username,email=email)
                    user.save()
                    refresh = RefreshToken.for_user(user)

                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    return Response({"message": "User created successfully.","data":token}, status=status.HTTP_200_OK)
                
                elif phone_number and otp_verification.objects.filter(phone_number=phone_number,otp=otp,expires_at__gte=timezone.now()).first():
                    user=User.objects.create_user(username=username,email=email)
                    user.save()
                    userpersonal=userpersonalinfo.objects.create(user=user,phone_number=phone_number)
                    userpersonal.save()
                    refresh = RefreshToken.for_user(user)

                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    return Response({"message": "User created successfully.","data":token}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class google_signin(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=google_profile(data=data)
            if serializers.is_valid():
                email=serializers.data.get('email')
                username=serializers.data.get('username')
                if User.objects.filter(email=email).exists():
                    return Response({"error": "user already exists."}, status=status.HTTP_400_BAD_REQUEST)       
                user=User.objects.create_user(username=username,email=email)
                user.save()
                if serializers.data.get('profile_pic'):
                    userpersonal=userpersonalinfo.objects.create(user=user,image_url=serializers.data.get('profile_pic'))
                    userpersonal.save()
                    
                refresh = RefreshToken.for_user(user)

                token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }
                return Response({"message": "User created successfully.","data":token}, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)            
                    

class login(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=login_serializer(data=data)
            if serializers.is_valid():
                email=serializers.data.get('email')
                phone_number=serializers.data.get('phone_number')    
                if email and User.objects.filter(email=email).exists():
                    email_sent,error_msg=send_otp_email(email,otp)
                    if error_msg:
                        return Response({"error": "otp not sent"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    expiry_time = timezone.now() + timezone.timedelta(seconds=30)
                    otp_instance = otp_verification.objects.filter(email=email).first()
                    #checking if already otp is present for the email
                    if otp_instance:
                        otp_instance.delete()
                        otp_verification.objects.create(email=email,otp=otp,expires_at=expiry_time)
                    else:
                        otp_verification.objects.create(email=email,otp=otp,expires_at=expiry_time)
                        request.session['details'] = serializers.validated_data
                    
                    t = threading.Thread(target=delete_expired_otp, args=(email,))
                    t.start()
                    
                    data={
                        "email":email,
                        "phone_number":phone_number
                    }
                    return JsonResponse({'message':'otp sent successfully to email',"data":data})
                
                elif phone_number and userpersonalinfo.objects.filter(phone_number=phone_number).exists():
                    phone_number_sent,error_msg=send_otp_email(phone_number,otp)
                    if error_msg:
                        return JsonResponse({'messages':error_msg},status=status.HTTP_400_BAD_REQUEST)
                    expiry_time = timezone.now() + timezone.timedelta(seconds=30)
                    
                    otp_instance = otp_verification.objects.filter(phone_number=phone_number).first()
                    #checking if already otp is present for the email
                    if otp_instance:
                        otp_instance.delete()
                        otp_verification.objects.create(phone_number=phone_number,otp=otp,expires_at=expiry_time)
                    else:
                        otp_verification.objects.create(phone_number=phone_number,otp=otp,expires_at=expiry_time)    
                    
                    data={
                        "email":email,
                        "phone_number":phone_number
                    }
                    
                    t = threading.Thread(target=delete_expired_otp, args=(phone_number,))
                    t.start()
                    return JsonResponse({'message':'otp sent successfully to phone number',"data":data},status=status.HTTP_200_OK)
                else:
                    return Response({"error": "user not found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)   
        
        
class otp_verification_login(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=otp_serializer(data=data)
            if serializers.is_valid():
                otp=serializers.data.get('otp')
                email=serializers.data.get('email')
                phone_number=serializers.data.get('phone_number')
                if not otp:
                    return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                if email and otp_verification.objects.filter(email=email,otp=otp,expires_at__gte=timezone.now()).first():
                    user=User.objects.get(email=email)
                    refresh = RefreshToken.for_user(user)

                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    return Response({"message": "User login successfully.","data":token}, status=status.HTTP_200_OK)
                
                elif phone_number and otp_verification.objects.filter(phone_number=phone_number,otp=otp,expires_at__gte=timezone.now()).first():
                    user=User.objects.get(phone_number=phone_number)
                    refresh = RefreshToken.for_user(user)

                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    return Response({"message": "User login successfully.","data":token}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class googlelogin(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=login_serializer(data=data)
            if serializers.is_valid():
                email=serializers.data.get('email')
                if User.objects.filter(email=email).exists():
                    user=User.objects.get(email=email)
                    refresh = RefreshToken.for_user(user)

                    token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                    return Response({"message": "User login successfully.","data":token}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "user not found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
