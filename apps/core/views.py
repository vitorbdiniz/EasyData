from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import UploadCsvSerializer


class UploadCsv(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_serializer = UploadCsvSerializer(data=request.data, context={'user': request.user})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
