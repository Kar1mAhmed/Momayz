from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import Package
from .serializers import PackageSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_packages(request):
    
    packages = Package.objects.all()
    serialized_packages = PackageSerializer(packages, many=True)
    return Response(serialized_packages.data, status=status.HTTP_200_OK)