from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Entrada(APIView):
    
    def post(self, request):
        return Response(request.data, status=status.HTTP_200_OK)
