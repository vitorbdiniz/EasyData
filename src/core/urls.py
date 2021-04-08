from django.urls import path
from core.views import Entrada

urlpatterns = [
    path('', Entrada.as_view(), name='teste'),
]
