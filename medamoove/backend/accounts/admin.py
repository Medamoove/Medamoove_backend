from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(otp_verification)
admin.site.register(userpersonalinfo)
admin.site.register(usermedicalinfo)
admin.site.register(lifestyleinfo)
admin.site.register(occupation)
admin.site.register(chronic_diseases)
admin.site.register(surgeries)
admin.site.register(injuries)
admin.site.register(Medication)
admin.site.register(Allergy)