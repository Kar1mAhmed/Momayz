from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import random
from .models import *


# Will be in app settings model
OTP_LIMIT_FOR_NUMBER = 20 
OTP_LIMIT_FOR_NUMBER_PER_DAY = 10
OTP_LIMIT_FOR_NUMBER_PER_HOUR = 5


def check_spam(phone):
    otps_of_number = OTP.objects.filter(phone=phone)
    now = datetime.now()

    if otps_of_number.count() > OTP_LIMIT_FOR_NUMBER:
        return True, "Phone number exceeded all OTPS limit."
    elif otps_of_number.filter(created_at__date=now.date()).count() > OTP_LIMIT_FOR_NUMBER_PER_DAY:
        return True, "Phone number exceeded today OTPS limit, try agin tomorrow. "
    elif otps_of_number.filter(created_at__date=now.time()).count() > OTP_LIMIT_FOR_NUMBER_PER_HOUR:
        return True, "Phone number exceeded This Hour OTPS limit, try agin after one hour."
    else:
        False
    
def send_otp(phone):
    otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp_code = '555555' # should be removed
    #send_otp_to_number(otp, phone)
    otp = OTP.objects.create(code=otp_code, phone=phone)
    otp.save()
    return True


@api_view(['POST'])
def generate_otp(request):
    phone_number = request.GET.get("phone_number")
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
    phone_number = request.GET.get("phone_number")
    otp_code = request.GET.get("code")
    
    otps = OTP.objects.filter(phone=phone_number)
    last_otp = otps.last()
    if not last_otp:
        return Response({'detail': "No OTP found for this phone number."}, status=status.HTTP_400_BAD_REQUEST)
    
    if last_otp.code == otp_code:
        time_difference = datetime.now() - last_otp.created_at
        if time_difference < timedelta(minutes=15):
            return({'detail': "OTP expired."}, status.HTTP_400_BAD_REQUEST)
        else:
            otps.delete()
            return Response({'detail': "Verified."}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "Wrong OTP."})
    

