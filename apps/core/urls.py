from django.urls import path
from apps.core.views import upload, dashboard, statistics, user_config

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('user/', user_config, name='user'),
    path('upload/', upload, name='upload'),
    path('statistics/<int:file_id>/', statistics, name='statistics'),
]
