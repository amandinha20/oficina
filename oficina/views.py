from django.shortcuts import render, redirect
from django.http import HttpResponse

USUARIO_FIXO = 'admin'
SENHA_FIXA = '1234'

def login(request):
    if request.session.get('logado'):
        return redirect('principal')
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        if usuario == USUARIO_FIXO and senha == SENHA_FIXA:
            request.session['logado'] = True
            return redirect('principal')
        else:
            return render(request, 'oficina/login.html', {'erro': 'Usuário ou senha inválidos.'})
    return render(request, 'oficina/login.html')

def principal(request):
    if not request.session.get('logado'):
        return redirect('login')
    return render(request, 'oficina/principal.html')

def home(request):
    if not request.session.get('logado'):
        return redirect('login')
    return render(request, 'oficina/home.html')
