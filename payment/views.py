from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import hashlib
import hmac


from users.models import User
from .models import Payment

from project.settings import HMAC_KEY

@api_view(['POST'])
def pay(request):
    if not HMAC_authentication(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # user_phone = request.request.data['obj']['payment_key_claims']['billing_request.data']['phone_number']
    # req_data = collect_required(request.request.data)
    # try:
    #     user = User.objects.get(username=user_phone)
    # except:
    #     Payment.objects.create(request)
        
    return Response(status=status.HTTP_200_OK)



def HMAC_authentication(request):
    values = [
        str(request.data['obj']['amount_cents']),
        request.data['obj']['created_at'],
        request.data['obj']['currency'],
        str(request.data['obj']['error_occured']).lower(),
        str(request.data['obj']['has_parent_transaction']).lower(),
        str(request.data['obj']['id']),
        str(request.data['obj']['integration_id']),
        str(request.data['obj']['is_3d_secure']).lower(),
        str(request.data['obj']['is_auth']).lower(),
        str(request.data['obj']['is_capture']).lower(),
        str(request.data['obj']['is_refunded']).lower(),
        str(request.data['obj']['is_standalone_payment']).lower(),
        str(request.data['obj']['is_voided']).lower(),
        str(request.data['obj']['order']['id']),
        str(request.data['obj']['owner']),
        str(request.data['obj']['pending']).lower(),
        str(request.data['obj']['source_data']['pan']),
        str(request.data['obj']['source_data']['sub_type']),
        str(request.data['obj']['source_data']['type']),
        str(request.data['obj']['success']).lower()]
        
    
    concatenated_string  = ''.join(values)

    hashed_message = hmac.new(
    key=HMAC_KEY.encode('utf-8'),
    msg=concatenated_string.encode('utf-8'),
    digestmod=hashlib.sha512).hexdigest()
    
    received_hash = request.GET.get('hmac')

    
    if hashed_message == received_hash:
        return True
    
    return False
