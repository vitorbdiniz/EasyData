from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('register/', views.register_page, name='register'),
]
