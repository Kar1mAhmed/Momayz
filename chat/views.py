from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Chat, Message
from .serializers import MessageSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_chat(request):
    user = request.user
    chat = get_object_or_404(Chat, user=user)
    messages = Message.objects.filter(chat=chat)
    serialized_data = MessageSerializer(messages)
    return Response(serialized_data.data, status=status.HTTP_200_OK)