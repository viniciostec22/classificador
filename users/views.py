from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def new_user(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "Senha e confirmar senha não coíncidem")
            return redirect('/users/new_user')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, "Usuário já existe")
            print("teste")
            return redirect('/users/new_user')
        try:
            User.objects.create_user(
                username=username,
                password=senha,
                email=email
                
            )
            return redirect('/users/login/')
        except:
            messages.add_message(request, constants.ERROR, "Erro interno do servidor")
            return redirect('/users/new_user')
    
def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, "Logado!!")
            # return redirect('/flashcard/novo_flashcard/')
            return redirect('/images/new_images/')
        else:
            messages.add_message(request, constants.ERROR, "Usuario ou senha invalidos")
            return redirect('/users/login/')
        
def logout(request):
    auth.logout(request)
    return redirect('/users/login/')