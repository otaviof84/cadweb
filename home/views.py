from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')


def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)


def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('categoria')
        else:
            messages.error(request, 'Erro ao cadastrar categoria. Verifique os dados.')
    else:
        form = CategoriaForm()

    return render(request, 'categoria/formulario.html', {'form': form})


def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
        return redirect('categoria')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categoria')
        else:
            messages.error(request, 'Erro ao atualizar categoria.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria/formulario.html', {'form': form})


def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso!')
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')

    return redirect('categoria')


def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
        return redirect('categoria')

    return render(request, 'categoria/detalhes.html', {'categoria': categoria})




