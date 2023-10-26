from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Message
from .serializers import MessageSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_chat(request):
    user = request.user
    messages = Message.objects.filter(user=user)
    serialized_data = MessageSerializer(messages, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)