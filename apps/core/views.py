from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.core.models import Sample
from apps.core.serializers import RegisterSerializer, AuthenticateSerializer


class Register(APIView):

    def post(self, request):
        file_serializer = RegisterSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Authenticate(APIView):

    def post(self, request):
        file_serializer = AuthenticateSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
