from django import forms
from .models import Listas, Itens


class ListasForm(forms.ModelForm):
    class Meta:
        model = Listas
        fields = ['nome']


class ItensForm(forms.ModelForm):
    class Meta:
        model = Itens
        fields = ['nome']
