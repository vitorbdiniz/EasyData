from django.urls import path
from apps.users.views import register, login_user, logout_user, forgot, reset_password

urlpatterns = [
    path('register/', register, name='register'),
    path('forgot/', forgot, name='forgot_password'),
    path('reset/<uidb64>/<token>', reset_password, name='reset_password'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
