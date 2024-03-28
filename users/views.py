from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
import re
from django.contrib.auth.decorators import login_required

@login_required
def new_user(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        # Verificar se o e-mail é válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.add_message(request, constants.ERROR, "E-mail inválido")
            return redirect('/users/new_user')
        
        # Verificar se a senha tem no mínimo 6 caracteres
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "Senha deve ter no mínimo 6 caracteres")
            return redirect('/users/new_user')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "Senha e confirmar senha não coincidem")
            return redirect('/users/new_user')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "Usuário já existe")
            return redirect('/users/new_user')
        
        try:
            user = User.objects.create_user(
                username=username,
                password=senha,
                email=email
            )
            messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso")
            return redirect('/users/login/')
        except Exception as e:
            messages.add_message(request, constants.ERROR, "Erro interno do servidor")
            print(e)  # Exibe o erro no console para fins de depuração
            return redirect('/users/new_user')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, "Logado com sucesso!")
            return redirect('/images/new_images/')
        else:
            messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
            return redirect('/users/login/')
        
def logout(request):
    auth.logout(request)
    return redirect('/users/login/')