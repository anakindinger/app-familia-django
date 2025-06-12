from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Child, School, Health
from .forms import ChildForm
from usuario.models import UsuarioChild
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from agenda.models import Evento
from rotina.models import Routine
from django.urls import reverse

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
    response = "Você está visualizando a lista de crianças com id %s."
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

@login_required
def recados(request):
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    pendentes = []
    # Rotinas pendentes
    for r in Routine.objects.filter(child_id__in=children_ids, status='pendente'):
        pendentes.append({
            'tipo': 'rotina',
            'obj': r,
            'url': reverse('rotina:aprovar_rotina', args=[r.id]) + f'?child_id={r.child_id}'
        })
    # Eventos pendentes
    for e in Evento.objects.filter(child_id__in=children_ids, status='pendente'):
        pendentes.append({
            'tipo': 'evento',
            'obj': e,
            'url': reverse('agenda:aprovar_evento', args=[e.id]) + f'?child_id={e.child_id}'
        })
    # School pendentes
    for s in School.objects.filter(child_id__in=children_ids, status='pendente'):
        pendentes.append({
            'tipo': 'school',
            'obj': s,
            'url': reverse('dashboard:aprovar_school', args=[s.id]) + f'?child_id={s.child_id}'
        })
    # Health pendentes
    for h in Health.objects.filter(child_id__in=children_ids, status='pendente'):
        pendentes.append({
            'tipo': 'health',
            'obj': h,
            'url': reverse('dashboard:aprovar_health', args=[h.id]) + f'?child_id={h.child_id}'
        })
    # Últimas atualizações aprovadas
    ultimas = []
    for e in Evento.objects.filter(child_id__in=children_ids, status='aprovado').order_by('-date', '-hour_init')[:3]:
        ultimas.append({'tipo': 'evento', 'obj': e})
    for r in Routine.objects.filter(child_id__in=children_ids, status='aprovado').order_by('-start_day', '-start_time')[:3]:
        ultimas.append({'tipo': 'rotina', 'obj': r})
    for s in School.objects.filter(child_id__in=children_ids, status='aprovado').order_by('-id')[:1]:
        ultimas.append({'tipo': 'school', 'obj': s})
    for h in Health.objects.filter(child_id__in=children_ids, status='aprovado').order_by('-id')[:1]:
        ultimas.append({'tipo': 'health', 'obj': h})
    def get_sort_date(obj):
        # Retorna uma data para ordenação, ou um valor mínimo se None
        d = getattr(obj, 'date', None)
        if d is not None:
            return d
        d = getattr(obj, 'start_day', None)
        if d is not None:
            return d
        # Retorna uma data antiga para garantir que None fique no final
        from datetime import date as _date
        return _date(1900, 1, 1)
    ultimas = sorted(ultimas, key=lambda x: get_sort_date(x['obj']), reverse=True)[:5]
    context = {'pendentes': pendentes, 'ultimas': ultimas}
    return render(request, 'dashboard/recados.html', context)

def get_child_context(request):
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    children = Child.objects.filter(id__in=children_ids)
    child_id = request.GET.get('child_id')
    if child_id and child_id.isdigit() and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
    else:
        selected_child = children.first() if children else None
    return {'children': children, 'selected_child': selected_child}

@login_required
def aprovar_school(request, school_id):
    school = get_object_or_404(School, id=school_id)
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if school.child_id not in children_ids:
        return redirect('dashboard:index')
    if request.method == 'POST' and school.status == 'pendente':
        school.status = 'aprovado'
        school.save()
    return redirect('dashboard:recados')

@login_required
def aprovar_health(request, health_id):
    health = get_object_or_404(Health, id=health_id)
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if health.child_id not in children_ids:
        return redirect('dashboard:index')
    if request.method == 'POST' and health.status == 'pendente':
        health.status = 'aprovado'
        health.save()
    return redirect('dashboard:recados')