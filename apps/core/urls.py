from django.urls import path
from apps.core.views import UploadCsv

urlpatterns = [
    path('upload', UploadCsv.as_view(), name='upload'),
]
