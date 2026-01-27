from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse



@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso!')
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')

    return redirect('categoria')

@login_required(login_url='login')
def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
        return redirect('categoria')

    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

@login_required(login_url='login')
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)

@login_required(login_url='login')
def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente')
        else:
            messages.error(request, 'Erro ao cadastrar cliente.')
    else:
        form = ClienteForm()

    return render(request, 'cliente/formulario.html', {'form': form})

@login_required(login_url='login')
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente')
        else:
            messages.error(request, 'Erro ao atualizar cliente.')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/formulario.html', {'form': form})

@login_required(login_url='login')
def remover_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    cliente.delete()
    messages.success(request, 'Cliente removido com sucesso!')
    return redirect('cliente')

@login_required(login_url='login')
def produto(request):
    return render(request, 'produto/lista.html', {'lista': Produto.objects.all()})

@login_required(login_url='login')
def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/form.html', {'form': form})

@login_required(login_url='login')
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})

@login_required(login_url='login')
def teste1(request):
    return render(request, 'testes/teste1.html')


@login_required(login_url='login')
def teste2(request):
    return render(request, 'testes/teste2.html')

def autocomplete_cliente(request):
    termo = request.GET.get('term', '')

    clientes = Cliente.objects.filter(
        nome__icontains=termo
    )[:10]

    dados = []

    for cliente in clientes:
        dados.append({
            'id': cliente.id,
            'label': cliente.nome,
            'value': cliente.nome
        })

    return JsonResponse(dados, safe=False)

@login_required(login_url='login')
def lista_pedido(request):
    pedidos = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': pedidos})

@login_required(login_url='login')
def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido')
    else:
        form = PedidoForm()

    return render(request, 'pedido/form.html', {'form': form})

@login_required(login_url='login')
def detalhes_pedido(request, id):
    pedido = get_object_or_404(Pedido, pk=id)
    itens = ItemPedido.objects.filter(pedido=pedido)

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.valor = item.produto.preco
            item.save()
            return redirect('detalhes_pedido', id=pedido.id)
    else:
        form = ItemPedidoForm()

    contexto = {
        'pedido': pedido,
        'itens': itens,
        'form': form,
    }

    return render(request, 'pedido/detalhes.html', contexto)

def detalhes_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    itens = ItemPedido.objects.filter(pedido=pedido)

    total = 0
    for item in itens:
        total += item.quantidade * item.valor

    pedido.total = total
    pedido.save()

    return render(request, 'pedido/detalhes.html', {
        'pedido': pedido,
        'itens': itens,
        'total': total
    })

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')










