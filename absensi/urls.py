from django.urls import path
from . import views

urlpatterns = [
    path('', views.absensi_home, name='absensi_home'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/tutor/<int:tutor_id>/absensi/', views.admin_tutor_absensi, name='admin_tutor_absensi'),
]
