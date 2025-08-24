from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date

from .forms import AbsensiForm
from .models import Absensi


def LoginView(request):  
    return render(request, "registration/login.html", {
        'now': timezone.now()
    })


@login_required
def absensi_home(request):
    """Gabungan Form Absensi + Daftar Absensi"""
    # --- Handle Form ---
    if request.method == "POST":
        form = AbsensiForm(request.POST, request.FILES)
        if form.is_valid():
            absensi = form.save(commit=False)
            absensi.tutor = request.user
            today = timezone.now().date()

            # Cek apakah tutor sudah absen hari ini
            if Absensi.objects.filter(tutor=request.user, tanggal=today).exists():
                messages.warning(
                    request,
                    f"Anda sudah mengisi absensi pada tanggal {today.strftime('%d %B %Y')}."
                )
                return redirect("absensi_home")

            absensi.tanggal = today
            absensi.save()
            messages.success(request, "Absensi berhasil ditambahkan.")
            return redirect("absensi_home")
    else:
        form = AbsensiForm()

    # --- Handle List ---
    today = date.today()
    bulan = today.month
    tahun = today.year

    if not request.user.is_staff:
        absensi_qs = Absensi.objects.filter(
            tutor=request.user,
            tanggal__month=bulan,
            tanggal__year=tahun
        ).order_by('-id')
    else:
        absensi_qs = Absensi.objects.all().order_by('-id')

    paginator = Paginator(absensi_qs, 25)
    page_number = request.GET.get("page")
    absensi = paginator.get_page(page_number)

    # --- Hitung Rekap ---
    hadir_count = absensi_qs.filter(status="hadir").count()
    alfa_count = absensi_qs.filter(status="alpha").count()
    izin_count = absensi_qs.filter(status="izin").count()
    bisaroh = hadir_count * 35000  # contoh Rp.20.000 per hadir

    return render(request, "absensi/absen_tutor.html", {
        "form": form,
        "absensi": absensi,
        "hadir_count": hadir_count,
        "alfa_count": alfa_count,
        "izin_count": izin_count,
        "bisaroh": bisaroh,
    })
