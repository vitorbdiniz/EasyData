from django.urls import path
from apps.users.views import Register, Authenticate

urlpatterns = [
    # auth
    path('', Register.as_view(), name='register'),
    path('authenticate', Authenticate.as_view(), name='authenticate'),
]
