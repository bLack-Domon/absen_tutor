from django.contrib import admin
from .models import Absensi

class AbsensiAdmin(admin.ModelAdmin):
    list_display = ("tutor", "tanggal", "status")
    list_filter = ("status", "tanggal")
    search_fields = ("tutor__username",)

admin.site.register(Absensi, AbsensiAdmin)
