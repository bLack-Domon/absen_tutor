from django.urls import path
from . import views

urlpatterns = [
    path('', views.absensi_home, name='absensi_home'),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/birpen/", views.birpen_dashboard, name="birpen_dashboard"),
]
