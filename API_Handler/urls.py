from django.urls import path

from views import hello_reader


urlpatterns = [
    path('', hello_reader),
]