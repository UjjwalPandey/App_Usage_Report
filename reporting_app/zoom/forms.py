from django import forms

from .models import Zoom


class ZoomForm(forms.ModelForm):
    class Meta:
        model = Zoom
        fields = '__all__'
