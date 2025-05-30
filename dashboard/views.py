from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Child, School, Health
from .forms import ChildForm
from usuario.models import UsuarioChild
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    lista_criancas = Child.objects.order_by('name')
    template = loader.get_template('dashboard/index.html')
    context = {
        'lista_criancas': lista_criancas,
    }
    return render(request, 'dashboard/index.html', context)
# Create your views here.

def child_list(request, child_id):
    response = "Voê está visualizando a lista de crianças com id %s."
    return HttpResponse(response % child_id)

'''def child_detail(request, child_id):
    child = Child.objects.get(pk=child_id)
    school = School.objects.filter(child=child)
    health = Health.objects.filter(child=child)
    return render(request, 'dashboard/child_detail.html', {'child': child, 'school': school, 'health': health})'''

@login_required
def cadastrar_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save()
            # Associa o usuário logado à criança
            UsuarioChild.objects.create(user=request.user, child=child)
            return redirect('dashboard:lista_children')
    else:
        form = ChildForm()
    return render(request, 'dashboard/cadastrar_child.html', {'form': form})

@login_required
def associar_usuario_child(request, child_id):
    child = Child.objects.get(id=child_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'dashboard/associar_usuario.html', {'child': child, 'erro': 'Usuário não encontrado'})
        # Limite de 2 usuários por criança
        if UsuarioChild.objects.filter(child=child).count() >= 2:
            return render(request, 'dashboard/associar_usuario.html', {'child': child, 'erro': 'Limite de 2 usuários já atingido'})
        UsuarioChild.objects.get_or_create(user=user, child=child)
        return redirect('dashboard:lista_children')
    return render(request, 'dashboard/associar_usuario.html', {'child': child})