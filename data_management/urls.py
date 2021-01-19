from django.contrib import admin
from django.urls import path
from data_processing_app import views

urlpatterns = [
    path('', admin.site.urls),
    path('example', views.example),
]
