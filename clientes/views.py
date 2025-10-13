from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from django.urls import reverse

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {'clientes': clientes})

def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone, endereco=endereco)
        return redirect(reverse('clientes:lista'))
    return render(request, 'clientes/novo.html')

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.cpf = request.POST.get('cpf')
        cliente.telefone = request.POST.get('telefone')
        cliente.endereco = request.POST.get('endereco')
        cliente.save()
        return redirect(reverse('clientes:lista'))
    return render(request, 'clientes/editar.html', {'cliente': cliente})

def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect(reverse('clientes:lista'))
    return render(request, 'clientes/excluir.html', {'cliente': cliente})
