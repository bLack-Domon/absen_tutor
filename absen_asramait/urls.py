from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from absensi.views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('absensi.urls')),

    # auth custom
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]

# Tambahkan ini supaya gambar/logo bisa tampil saat DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
