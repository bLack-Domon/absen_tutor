from django import forms
from .models import Absensi

class CameraInput(forms.ClearableFileInput):
    def __init__(self, attrs=None):
        default_attrs = {'accept': 'image/*', 'capture': 'environment'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ["foto"]
        widgets = {
            "foto": CameraInput(),
        }
