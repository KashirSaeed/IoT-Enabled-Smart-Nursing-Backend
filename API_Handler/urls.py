# example/urls.py
from django.urls import path

from API_Handler.views import index,fetch_from_influx,count_influx,fetch_images_ids


urlpatterns = [
    path('', index),
    path('fetch/',fetch_from_influx),
    path('count/',count_influx),
    path('image_id/',fetch_images_ids)
    
]