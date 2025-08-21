from django.urls import path
from . import views

urlpatterns = [
    path('', views.absensi_create, name='absensi_create'),
    path('daftar-absensi/', views.absensi_list, name='absensi_list'),
]
