from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.absensi_create, name="absensi_create"),
    path("", views.absensi_list, name="absensi_list"),
]
