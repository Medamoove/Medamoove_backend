from django.shortcuts import render
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
import cloudinary.uploader


from django.shortcuts import redirect
""" from allauth.socialaccount.models import SocialAccount """

from .tests import *
from django.utils import timezone
import threading
from .models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from accounts.views import *
from accounts.models import *
import random
from accounts.serializers import *
# Create your views here.

class adddoctor(APIView):
    def post(self,request):
        try:
            user= get_user_from_token(request)
            print(user)
            if not user:
                return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            user_in=hopital_admin.objects.filter(user=user).first()
            print(user_in)
            if not user_in:
                return Response({"error":"not Authorized"},status=status.HTTP_400_BAD_REQUEST)
            hid=user_in.hospital
            data=request.data
            serializer=doctor_serializer(data=data)
            print(serializer)
            if serializer.is_valid():
                username=data['first_name']+data['last_name']+str(random.randint(1,1000))
                doctor=User.objects.create_user(username=username,email=data['email'])
                serializer.save(hid=hid,created_by=user,user=doctor)
                return Response("created successfully",status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
class getdoctors(APIView):
    def get(self,request):
        try:
            user= get_user_from_token(request)
            if not user:
                return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            user_in=hopital_admin.objects.filter(user=user).first()
            if not user_in:
                return Response({"error":"not Authorized"},status=status.HTTP_400_BAD_REQUEST)
            hid=user_in.hospital
            doctor=doctors.objects.filter(hid=hid)
            serializer=retrivedoctor_serializer(doctor,many=True)
            dataa=serializer.data
            for a in dataa:
                user=doctors.objects.get(docid=a['docid']).user
                userprofile=userpersonalinfo.objects.get(user=user).image_url
                a['profile_url']=userprofile
            return Response({"data":dataa},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class addpatient(APIView):
            def post(self,request):
                try:
                    user= get_user_from_token(request)
                    if not user:
                        return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
                    user_in=hopital_admin.objects.filter(user=user).first()
                    if not user_in:
                        return Response({"error":"not Authorized"},status=status.HTTP_400_BAD_REQUEST)
                    hid=user_in.hospital
                    data=request.data
                    serializer=patient_serializer(data=data)
                    if serializer.is_valid():
                        if User.objects.filter(email=data['email']).exists():
                            patient=User.objects.get(email=data['email'])
                        else:
                            username=data['first_name']+data['last_name']+str(random.randint(1,1000))
                            patient=User.objects.create_user(username=username,email=data['email'])    
                        
                        serializer.save(hid=hid,created_by=user,user=patient)    
                        return Response("created successfully",status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:    
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
class getpatients(APIView):
    def get(self,request):
        try:
            user= get_user_from_token(request)
            if not user:
                return Response({"error":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            user_in=hopital_admin.objects.filter(user=user).first()
            if not user_in:
                return Response({"error":"not Authorized"},status=status.HTTP_400_BAD_REQUEST)
            hid=user_in.hospital
            patients=patient.objects.filter(hid=hid)
            serializer=retrivepatient_serializer(patients,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)                
        

class addwallet_byadmin(APIView):
    def post(self,request):
        try:
            user = get_user_from_token(request)
            if not user:
                return Response({"error": "user not found."}, status=status.HTTP_400_BAD_REQUEST)
            user_in = hopital_admin.objects.filter(user=user).first()
            if not user_in:
                return Response({"error": "not Authorized"}, status=status.HTTP_400_BAD_REQUEST)
            data=request.data
            serializer=card_serializer(data=data)
            print(serializer)
            if serializer.is_valid():
                documents=request.FILES.getlist('documents')
                print(documents)
                data_list=[]
                if documents:
                    for doc in documents:
                        print(doc)
                        upload_result = cloudinary.uploader.upload(doc)
                        a=files.objects.create(file_url=upload_result['secure_url'],public_id=upload_result['public_id'])
                        data_list.append(a)
                    instance=serializer.save(created_by=user)
                    instance.files.set(data_list)
                else:
                    instance=serializer.save()    
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
            
            wallets=Wallet.objects.create(user=user)
            wallets.cards.add(instance)
            return Response({"message":"created successfully"},status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
                