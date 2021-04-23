from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.core.models import Sample
from apps.core.serializers import SampleSerializer

class Entrada(APIView):
    
    def post(self, request):
        return Response(request.data, status=status.HTTP_200_OK)


class Teste(APIView):

    def get(self, request):
        file_serialized = SampleSerializer(Sample.objects.all(), many=True)
        return Response(file_serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        file_serializer = SampleSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
