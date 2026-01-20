from django import forms
from .models import *
from datetime import date

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


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
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
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'datanasc': forms.DateInput(attrs={'class': 'form-control'}, format='%d/%m/%Y'),
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > date.today():
            raise forms.ValidationError('Data de nascimento não pode ser futura.')
        return datanasc
    
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['categoria', 'nome', 'preco', 'imagem']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'form-control preco'}),
            'imagem': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['status']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'status', 'total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control autocomplete'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.TextInput(attrs={'class': 'form-control money'}),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={
                'class': 'form-control autocomplete'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control inteiro'
            }),
        }


