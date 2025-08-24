from django.urls import path
from . import views

urlpatterns = [
    path('', views.absensi_home, name='absensi_home'),
]
