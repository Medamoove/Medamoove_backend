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
from accounts.views import login,otp_verification_login,googlelogin,personalinfo,medicalinfo,userlifestyleinfo
from accounts.views import *

from erp.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/profile/', google_login, name='google_login_token'),
    path('api/token/', CustomAuthTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/create_user/', create_user.as_view(), name='create_user'),
    path('api/verify_otp/', otp_verification_signin.as_view(), name='verify_otp'),
    path('api/google_signin/', google_signin.as_view(), name='google_login'),
    path('api/login/', login.as_view(), name='login'),
    path('api/verify_otp_login/', otp_verification_login.as_view(), name='verify_otp_login'),
    path('api/google_login/', googlelogin.as_view(), name='login'),
    path('api/getuserpersonalinfo/',personalinfo.as_view(),name='getuserpersonalinfo'),#get user personal info
    path('api/getusermedicalinfo/',medicalinfo.as_view(),name='getusermedicalinfo'),#get user medical info
    path('api/getlifestyleinfo/',userlifestyleinfo.as_view(),name='getlifestyleinfo'),#get lifestyle info
    path('api/updatepersonalinfo/',updateuserpersonalinfo.as_view(),name='updateuserpersonalinfo'), #update userpersonalinfo
    path('api/getdata/',getdata.as_view(),name='getdata'), #get data
    path('api/updateusermedicalinfo/',updateusermedicalinfo.as_view(),name='updateusermedicalinfo'), #update usermedicalinfo
    path('api/updatelifestyleinfo/',updatelifestyleinfo.as_view(),name='updatelifestyleinfo'), #update lifestyleinfo
    path('erp/adddoctor/',adddoctor.as_view(),name='adddoctor'), #add doctor
    path('erp/getdoctors/',getdoctors.as_view(),name='getdoctors'), #get doctors
    path('erp/getpatient/',getpatients.as_view(),name='getdoctor'), #get doctor
    path('erp/addpatient/',addpatient.as_view(),name='addpatient'), #add patient
    path('api/addwallet/',addwallet.as_view(),name='addwallet'), #add wallet by user
    path('api/getwallet/',getwallet.as_view(),name='getwallet'), #get wallet by user
    path('api/addwallet_admin/',addwallet_byadmin.as_view(),name='getwallet'), #get wallet by user
]    
