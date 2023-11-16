from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



@api_view(['POST'])
def pay(request):
    return Response(status=status.HTTP_200_OK)


def HMAC_authentication(request):
    pass
