from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import datetime
from django.utils import timezone
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
import re

import random
from .models import *
from users.models import User



# Will be in app settings model
OTP_LIMIT_FOR_NUMBER = 20 
OTP_LIMIT_FOR_NUMBER_PER_DAY = 10
OTP_LIMIT_FOR_NUMBER_PER_HOUR = 5
OTP_EXPIRATION_MIN = 15


def check_spam(phone_number):
    
    otps_of_number = OTP.objects.filter(phone_number=phone_number)
    now = datetime.datetime.now()
    
    if otps_of_number.count() >= OTP_LIMIT_FOR_NUMBER:
        return True, "Phone number exceeded all OTPS limit."
    if otps_of_number.filter(created_at__date=now.date()).count() >= OTP_LIMIT_FOR_NUMBER_PER_DAY:
        return True, "Phone number exceeded today OTPS limit, try agin tomorrow. "
    if otps_of_number.filter(created_at__hour=now.hour, created_at__date = now.date()).count() >= OTP_LIMIT_FOR_NUMBER_PER_HOUR:
        return True, "Phone number exceeded This Hour OTPS limit, try agin after one hour."
    else:
        return False, None
    
def send_otp(phone):
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp_code = '555555' # should be removed
    #send_otp_to_number(otp, phone)
    otp = OTP.objects.create(code=otp_code, phone_number=phone)
    otp.save()
    return True


@api_view(['POST'])
def generate_otp(request):
    phone_number = request.data['phone_number']
    reset = request.data.get('reset')
    
    if check_phone_exist(phone_number) and reset != True:
        return Response({'detail': 'الرقم مستخدم بالفعل.'}, status=status.HTTP_409_CONFLICT)
    
    if reset == True and not check_phone_exist(phone_number):
        return Response({"detail": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    
    if not is_egyptian_number(phone_number):
        return Response({"detail": "Wrong phone number."}, status=status.HTTP_400_BAD_REQUEST)
    
    spam, message = check_spam(phone_number)

    if spam:
        return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
    else:
        send = send_otp(phone_number)
        if send:
            return Response({"detail": "OTP sent successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "OTP send failed."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data["phone_number"]
    otp_code = request.data["code"]
        
    otps = OTP.objects.filter(phone_number=phone_number).order_by('-created_at')
    last_otp = otps.first()

    if not last_otp:
        return Response({'detail': "No OTP found for this phone number."}, status=status.HTTP_400_BAD_REQUEST)
    
    if last_otp.code == otp_code:
        if last_otp.is_expired():  
            return Response({'detail': "OTP expired."}, status.HTTP_400_BAD_REQUEST)
        else:
            otps = OTP.objects.filter(phone_number=phone_number).exclude(id=last_otp.id)
            otps.exclude(id=last_otp.id)
            return Response({'detail': "Verified."}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "Wrong OTP."})
    

    
def check_phone_exist(phone_number):
    try:
        user = User.objects.get(username=phone_number)
        # User with the specified phone number exists
        return True
    except ObjectDoesNotExist:
        # User with the specified phone number does not exist
        return False
    

    
def is_egyptian_number(phone_number):
    pattern = r'^(011|010|012|015)\d{8}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False    

