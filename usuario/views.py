from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# Tela de cadastro
def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuario:login')
    else:
        form = UserCreationForm()
    return render(request, 'usuario/cadastro.html', {'form': form})

# Tela de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:index')  # Redireciona para a página de boas-vindas
    else:
        form = AuthenticationForm()
    return render(request, 'usuario/login.html', {'form': form})

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('usuario:login')
