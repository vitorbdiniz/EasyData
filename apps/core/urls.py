from django.urls import path
from apps.core.views import upload, dashboard, statistics

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload, name='upload'),
    path('statistics/', statistics, name='statistics'),
]
