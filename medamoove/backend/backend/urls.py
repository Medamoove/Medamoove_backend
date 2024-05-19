"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import CustomAuthTokenView,google_login,create_user,otp_verification_signin,google_signin
from accounts.views import login,otp_verification_login,googlelogin




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', google_login, name='google_login_token'),
    path('api/token/', CustomAuthTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/create_user/', create_user.as_view(), name='create_user'),
    path('api/verify_otp/', otp_verification_signin.as_view(), name='verify_otp'),
    path('api/google_signin/', google_signin.as_view(), name='google_login'),
    path('api/login/', login.as_view(), name='login'),
    path('api/verify_otp_login/', otp_verification_login.as_view(), name='verify_otp_login'),
    path('api/google_login/', googlelogin.as_view(), name='login'),
]    
