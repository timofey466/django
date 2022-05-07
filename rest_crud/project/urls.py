"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from app.views import ProjectViewSet, Project_one, MeasurementViewSet, MeasurementUpdate, MeasurementPut

r = DefaultRouter()
r.register('post', MeasurementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/', ProjectViewSet.as_view()),
    path('views/<pk>/', Project_one.as_view()),
    path('patch/<pk1>/', MeasurementUpdate.as_view()),
    path('put/<pk2>/',  MeasurementPut.as_view()),
] + r.urls
