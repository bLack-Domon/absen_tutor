from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AbsensiForm
from .models import Absensi
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

def LoginView(request):  
    return render(request, "registration/login.html",
        {'now': timezone.now()}
    )

@login_required
def absensi_create(request):
    if request.method == "POST":
        form = AbsensiForm(request.POST, request.FILES)
        if form.is_valid():
            absensi = form.save(commit=False)
            absensi.tutor = request.user

            # Ambil tanggal hari ini
            today = timezone.now().date()

            # Cek apakah tutor sudah absen di tanggal hari ini
            if Absensi.objects.filter(tutor=request.user, tanggal=today).exists():
                messages.warning(request, f"Anda sudah mengisi absensi pada tanggal {today.strftime('%d %B %Y')}.")
                return redirect("absensi_list")

            absensi.save()
            messages.success(request, "Absensi berhasil ditambahkan.")
            return redirect("absensi_list")
    else:
        form = AbsensiForm()

    return render(request, "absensi/absensi_form.html", {"form": form})

@login_required
def absensi_list(request):
    # tutor hanya melihat absensinya sendiri
    if not request.user.is_staff:
        absensi_qs = Absensi.objects.filter(tutor=request.user).order_by('-id')
    else:
        # koordinator / admin bisa lihat semua
        absensi_qs = Absensi.objects.all().order_by('-id')

    # Pagination (10 data per halaman, bisa diubah)
    paginator = Paginator(absensi_qs, 2)  
    page_number = request.GET.get("page")
    absensi = paginator.get_page(page_number)

    return render(request, "absensi/absensi_list.html", {"absensi": absensi})