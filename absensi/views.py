from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AbsensiForm
from .models import Absensi
from django.utils import timezone

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
            absensi.save()
            return redirect("absensi_list")
    else:
        form = AbsensiForm()
    return render(request, "absensi/absensi_form.html", {"form": form})

@login_required
def absensi_list(request):
    # tutor hanya melihat absensinya sendiri
    if not request.user.is_staff:
        absensi = Absensi.objects.filter(tutor=request.user)
    else:
        # koordinator / admin bisa lihat semua
        absensi = Absensi.objects.all()
    return render(request, "absensi/absensi_list.html", {"absensi": absensi})
