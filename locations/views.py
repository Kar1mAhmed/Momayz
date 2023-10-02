
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CitySerializer, GovernSerializer
from .models import City, Govern




class GovernView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        governs = Govern.objects.all()
        serialized_data = GovernSerializer(governs, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    



class CityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        requested_govern = request.GET.get('govern_id')
        if requested_govern is None:
            return Response({'detail': 'Please provide the "govern" value in query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        cites = City.objects.filter(govern=requested_govern)
        serialized_data = CitySerializer(cites, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    
