from django import forms
from .models import Listas


class ListasForm(forms.ModelForm):
    class Meta:
        model = Listas
        fields = ['nome']
