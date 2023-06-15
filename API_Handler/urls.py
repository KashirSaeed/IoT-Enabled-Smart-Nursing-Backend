# example/urls.py
from django.urls import path

from API_Handler.views import index,fetch_from_influx,count_influx
from API_Handler.signIn import getSpecificUser
from API_Handler.signUp import postUserData

urlpatterns = [
    path('', index),
    path('fetch/',fetch_from_influx),
    path('count/',count_influx),
    path('userData/',postUserData),
    path('user/<str:email>/<str:password>/<str:isAuthenticatedByGoogle>/',getSpecificUser),
]