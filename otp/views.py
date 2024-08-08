from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import OTP
from .helpers import *


@api_view(['POST'])
def generate_otp(request):
    # phone_number = request.data['phone_number']
    email = request.data['email']
    reset = request.data.get('reset')
    
    if check_email_exist(email) and reset != True:
        return Response({'detail': 'الرقم مستخدم بالفعل.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if reset == True and not check_email_exist(email):
        return Response({"detail": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    
    # if not is_egyptian_number(phone_number):
    #     return Response({"detail": "Wrong phone number."}, status=status.HTTP_400_BAD_REQUEST)
    
    # spam, message = check_spam(email)

    # if spam:
    #     return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
    send = send_otp(email)
    if send:
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "OTP send failed."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    email = request.data["email"]
    otp_code = request.data["code"]
        
    otps = OTP.objects.filter(email=email).order_by('-created_at')
    last_otp = otps.first()

    if not last_otp:
        return Response({'detail': "No OTP found for this phone number."}, status=status.HTTP_400_BAD_REQUEST)
    
    if last_otp.code == otp_code:
        if last_otp.is_expired():  
            return Response({'detail': "OTP expired."}, status.HTTP_400_BAD_REQUEST)
        else:
            otps = OTP.objects.filter(email=email).exclude(id=last_otp.id)
            otps.exclude(id=last_otp.id)
            return Response({'detail': "Verified."}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "Wrong OTP."})
