from django import forms
from .models import *

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if nome is None or len(nome) < 3:
            raise forms.ValidationError('O nome da categoria deve ter no mínimo 3 caracteres.')

        return nome

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')

        if ordem is None or ordem < 1:
            raise forms.ValidationError('A ordem deve ser maior que zero.')

        return ordem
