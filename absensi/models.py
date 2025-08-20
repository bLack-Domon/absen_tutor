from django.db import models
from django.contrib.auth.models import User

class Absensi(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="absensi")
    tanggal = models.DateField(auto_now_add=True)
    foto = models.ImageField(upload_to="absensi_foto/")

    status = models.CharField(
        max_length=20,
        choices=[
            ("menunggu", "Menunggu Verifikasi"),
            ("hadir", "Hadir"),
            ("izin", "Izin"),
            ("alpha", "Alpha"),
        ],
        default="menunggu"
    )
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tutor.username} - {self.tanggal}"
