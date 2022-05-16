from django.urls import path
from .views import *

app_name='account'

urlpatterns = [
    path('login', Login.as_view(), name='login-view'),
    path('info', Info.as_view()),
    path('token', GetToken.as_view())
]