from django.urls import path
from apps.core.views import StatisticsCsv, StatisticsCalculate

urlpatterns = [
    path('statistics', StatisticsCsv.as_view(), name='statistics-csv'),
    path('statistics/<int:csv_id>', StatisticsCalculate.as_view(), name='statistics'),
]
