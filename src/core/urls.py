from django.urls import path
from core.views import Entrada, Teste

urlpatterns = [
    path('', Entrada.as_view(), name='teste'),
    path('sample', Teste.as_view(), name='sample'),
]
