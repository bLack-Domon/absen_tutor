from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from datetime import date

from .forms import AbsensiForm
from .models import Absensi


class CustomLoginView(DjangoLoginView):
    """LoginView custom dengan redirect sesuai group"""
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="admin").exists():
            return reverse_lazy("admin_dashboard")
        elif user.groups.filter(name="birpen").exists():
            return reverse_lazy("birpen_dashboard")
        elif user.groups.filter(name="tutor").exists():
            return reverse_lazy("absensi_home")
        else:
            messages.error(self.request, "Anda tidak memiliki akses!")
            return reverse_lazy("login")


@login_required
def absensi_home(request):
    """Gabungan Form Absensi + Daftar Absensi"""

    # hanya tutor yang boleh masuk
    if not request.user.groups.filter(name="tutor").exists():
        if request.user.groups.filter(name="admin").exists():
            return redirect("admin_dashboard")
        elif request.user.groups.filter(name="birpen").exists():
            return redirect("birpen_dashboard")
        messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
        return redirect("login")

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

    absensi_qs = Absensi.objects.filter(
        tutor=request.user,
        tanggal__month=bulan,
        tanggal__year=tahun
    ).order_by('-id')

    paginator = Paginator(absensi_qs, 25)
    page_number = request.GET.get("page")
    absensi = paginator.get_page(page_number)

    # --- Hitung Rekap ---
    hadir_count = absensi_qs.filter(status="hadir").count()
    alfa_count = absensi_qs.filter(status="alpha").count()
    izin_count = absensi_qs.filter(status="izin").count()
    bisaroh = hadir_count * 35000  # contoh Rp.35.000 per hadir

    return render(request, "absensi/absen_tutor.html", {
        "form": form,
        "absensi": absensi,
        "hadir_count": hadir_count,
        "alfa_count": alfa_count,
        "izin_count": izin_count,
        "bisaroh": bisaroh,
    })


# --- Helper cek group ---
def is_admin(user):
    return user.groups.filter(name="admin").exists()


def is_birpen(user):
    return user.groups.filter(name="birpen").exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "dashboard/admin.html")


@login_required
@user_passes_test(is_birpen)
def birpen_dashboard(request):
    return render(request, "dashboard/birpen.html")
