from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

def otp_generator():
    import random
    return random.randint(1000, 9999)

otp = otp_generator()
def send_otp_email(email,otp):
    try:
        subject='email verification otp'
        message=f'your otp is {otp}'
        from_email='rahul2210085@akgec.ac.in'
        recipient_list=[email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return True,None
    except ValidationError:
        # If email address is invalid, return error response
        return False, 'Invalid email address'
    except Exception as e:
        # If other errors occur during email sending, return error response
        return False, str(e)

# Create your tests here.
