from .models import OTP
from users.models import User

import pytz
from datetime import timedelta
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


import re
import random


# Will be in app settings model
OTP_LIMIT_FOR_NUMBER = 20 
OTP_LIMIT_FOR_NUMBER_PER_DAY = 10
OTP_LIMIT_FOR_NUMBER_PER_HOUR = 5
OTP_EXPIRATION_MIN = 15


# Function to delete old OTPs
def delete_old_otps(passed_days=1):
    """
    Delete OTPs older than a specified number of days.

    Args:
        passed_days (int): Number of days for OTP expiration. Defaults to 1.
    """
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    deletion_date = current_date - timedelta(days=passed_days)

    # Delete old OTPs
    OTP.objects.filter(created_at__lt=deletion_date).delete()
    
    
# def check_spam(email):
    
#     otps_of_number = OTP.objects.filter(email=email)
#     now = datetime.datetime.now()
    
#     if otps_of_number.count() >= OTP_LIMIT_FOR_NUMBER:
#         return True, "Phone number exceeded all OTPS limit."
#     if otps_of_number.filter(created_at__date=now.date()).count() >= OTP_LIMIT_FOR_NUMBER_PER_DAY:
#         return True, "Phone number exceeded today OTPS limit, try agin tomorrow. "
#     if otps_of_number.filter(created_at__hour=now.hour, created_at__date = now.date()).count() >= OTP_LIMIT_FOR_NUMBER_PER_HOUR:
#         return True, "Phone number exceeded This Hour OTPS limit, try agin after one hour."
#     else:
#         return False, None
    
def send_otp(email):
    print('Sending otp phase started')
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    #send_otp_to_number(otp, phone)
    try: 
        send_otp_to_email(email, otp_code)
        otp = OTP.objects.create(code=otp_code, email=email)
        otp.save()
        return True
    except Exception as e:
        print(e)
        return False


def send_otp_to_email(email, otp):
    subject = 'Email verification'
    message = f'This is Your OTP for Momayz app: {otp}'
    from_email = 'basketserviceteam@gmail.com'
    recipient_list = [f'{email}']
    print(recipient_list)
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
def check_email_exist(email):
    try:
        user = User.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False
    

    
def is_egyptian_number(phone_number):
    pattern = r'^(011|010|012|015)\d{8}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False    
