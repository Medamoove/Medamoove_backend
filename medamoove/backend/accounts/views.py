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
from allauth.socialaccount.models import SocialAccount

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
