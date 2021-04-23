from django.urls import path
from apps.core.views import Register, Authenticate

urlpatterns = [
    # auth
    path('users/register', Register.as_view(), name='register'),
    path('users/authenticate', Authenticate.as_view(), name='authenticate'),
]
