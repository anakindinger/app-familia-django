from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Child, School, Health
from .forms import ChildForm
from usuario.models import UsuarioChild
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    # Filtra apenas as crianças associadas ao usuário
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    children = Child.objects.filter(id__in=children_ids).order_by('name')
    # Seleciona a criança ativa
    child_id = request.GET.get('child_id')
    if child_id and child_id.isdigit() and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
    else:
        selected_child = children.first() if children else None
    perfil = None
    if selected_child:
        escola = School.objects.filter(child=selected_child).first()
        saude = Health.objects.filter(child=selected_child).first()
        from agenda.models import Evento
        from rotina.models import Routine
        ultimos_eventos = Evento.objects.filter(child=selected_child).order_by('-date', '-hour_init')[:3]
        ultimas_rotinas = Routine.objects.filter(child=selected_child).order_by('-start_day', '-start_time')[:3]
        updates = list(ultimos_eventos) + list(ultimas_rotinas)
        updates.sort(key=lambda x: getattr(x, 'date', getattr(x, 'start_day', None)) or getattr(x, 'start_day', None), reverse=True)
        perfil = {
            'child': selected_child,
            'school': escola,
            'health': saude,
            'updates': updates[:3],
        }
    context = {
        'perfil': perfil,
        'children': children,
        'selected_child': selected_child,
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

def get_child_context(request):
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    children = Child.objects.filter(id__in=children_ids)
    child_id = request.GET.get('child_id')
    if child_id and child_id.isdigit() and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
    else:
        selected_child = children.first() if children else None
    return {'children': children, 'selected_child': selected_child}