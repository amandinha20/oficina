from django.shortcuts import render, redirect, get_object_or_404
from .models import Veiculo
from clientes.models import Cliente
from django.urls import reverse

def lista_veiculos(request):
    veiculos = Veiculo.objects.select_related('cliente').all()
    return render(request, 'veiculos/lista.html', {'veiculos': veiculos})

def novo_veiculo(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        placa = request.POST.get('placa')
        modelo = request.POST.get('modelo')
        ano = request.POST.get('ano')
        cor = request.POST.get('cor')
        quilometragem = request.POST.get('quilometragem')
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        Veiculo.objects.create(placa=placa, modelo=modelo, ano=ano, cor=cor, quilometragem=quilometragem, cliente=cliente)
        return redirect(reverse('veiculos:lista'))
    return render(request, 'veiculos/novo.html', {'clientes': clientes})

def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        veiculo.placa = request.POST.get('placa')
        veiculo.modelo = request.POST.get('modelo')
        veiculo.ano = request.POST.get('ano')
        veiculo.cor = request.POST.get('cor')
        veiculo.quilometragem = request.POST.get('quilometragem')
        cliente_id = request.POST.get('cliente')
        veiculo.cliente = get_object_or_404(Cliente, pk=cliente_id)
        veiculo.save()
        return redirect(reverse('veiculos:lista'))
    return render(request, 'veiculos/editar.html', {'veiculo': veiculo, 'clientes': clientes})

def excluir_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    if request.method == 'POST':
        veiculo.delete()
        return redirect(reverse('veiculos:lista'))
    return render(request, 'veiculos/excluir.html', {'veiculo': veiculo})
