from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser
from apps.core.services import statistics, data_conversion
from apps.core.models import CsvFile

from .serializers import UploadCsvSerializer


class StatisticsCsv(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_serializer = UploadCsvSerializer(data=request.data, context={'user': request.user})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_200_OK)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticsCalculate(APIView):

    def get(self, request, csv_id):
        csv_file = CsvFile.objects.get(id=csv_id)
        data_frame = data_conversion.csv_to_df(csv_file.file)
        result_serialized = {}
        params = self.request.query_params.get('statistics').split(',')
        if 'mean' in params:
            result_serialized['mean'] = statistics.mean(data_frame)
        if 'median' in params:
            result_serialized['median'] = statistics.median(data_frame)
        if 'variance' in params:
            result_serialized['variance'] = statistics.variance(data_frame)
        if 'standard_deviation' in params:
            result_serialized['standard_deviation'] = statistics.standard_deviation(data_frame)

        return Response(result_serialized, status=status.HTTP_200_OK)
