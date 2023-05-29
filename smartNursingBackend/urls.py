"""
URL configuration for smartNursingBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from API_Handler import views

urlpatterns = [
    # path('', include('API_Handler.urls')),
    path('admin/', admin.site.urls),
    path('',views.hello_reader, name="hello_reader"),
    # path('sse/', views.sse_endpoint, name='sse'),
    path('fetch/', views.fetch_from_influx, name='fetch_from_influx'),
]
