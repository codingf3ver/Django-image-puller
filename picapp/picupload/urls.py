from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('imagetag/', views.imagetag, name='imagetag'),
    path('imagetag/<int:id>', views.imagetag, name='imagetag'),
]