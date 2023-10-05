from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
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
        return True, "Phone number exceeded all otps limit."
    elif otps_of_number.filter(created_at__date=now.date()).count() > OTP_LIMIT_FOR_NUMBER_PER_DAY:
        return True, "Phone number exceeded today otps limit, try agin tomorrow. "
    elif otps_of_number.filter(created_at__date=now.time()).count() > OTP_LIMIT_FOR_NUMBER_PER_HOUR:
        return True, "Phone number exceeded This Hour otps limit, try agin after one hour."
    else:
        False
    
def send_otp(phone):
    #otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    otp_code = '555555'
    #send_otp_to_number(otp, phone)
    otp = OTP.objects.create(code=otp_code, phone=phone)
    otp.save()
    return True


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def generate_otp(request):
    phone_number = request.GET.get("phone_number")
    spam, message = check_spam(phone_number)
    
    if spam:
        return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
    else:
        send = send_otp(phone_number)
        if send:
            return Response({"detail": "Otp sent successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Otp send failed."}, status=status.HTTP_400_BAD_REQUEST)
