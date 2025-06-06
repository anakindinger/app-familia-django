from django.shortcuts import render, redirect, get_object_or_404
from .models import Routine, Weekday
from dashboard.models import Child
from usuario.models import UsuarioChild
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from dashboard.views import get_child_context

# Create your views here.
'''def list_routines(request):
    context = {
        'lista_rotinas': Routine.objects.all().order_by('start_time'),
    }
    return render(request, 'rotina/list_routines.html', context)'''

@login_required
def rotina_hoje(request):
    # Filtra apenas as crianças do usuário
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    # Seleção de criança
    child_id = request.GET.get('child_id')
    if child_id and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
    else:
        selected_child = Child.objects.filter(id__in=children_ids).first()
        child_id = selected_child.id if selected_child else None
    today = date.today()
    weekday_map = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7'}
    weekday_str = weekday_map[today.weekday()]
    tomorrow = (today.weekday() + 1) % 7
    weekday_tmr = weekday_map[tomorrow]
    routine_today = Routine.objects.filter(days_of_week__day=weekday_str, child_id=child_id).distinct().order_by('start_time') if child_id else []
    routine_tomorrow = Routine.objects.filter(days_of_week__day=weekday_tmr, child_id=child_id).distinct().order_by('start_time') if child_id else []
    dias_semana = Weekday.objects.all().order_by('day')
    todas_rotinas = Routine.objects.filter(child_id=child_id).order_by('start_time') if child_id else []
    # Lista de crianças do usuário
    context = {
        'rotina_hoje': routine_today,
        'data_atual': today,
        'rotina_amanha': routine_tomorrow,
        'dias_semana': dias_semana,
        'todas_rotinas': todas_rotinas,
    }
    context.update(get_child_context(request))
    return render(request, 'rotina/rotinas.html', context)

@csrf_exempt
@login_required
def cadastrar_rotina(request):
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if request.method == 'POST':
        descricao = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        dias = request.POST.getlist('days_of_week')
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        child_id = request.POST.get('child_id')
        if not child_id or int(child_id) not in children_ids:
            return redirect('rotina:rotina_hoje')
        rotina = Routine.objects.create(
            description=descricao,
            start_time=start_time,
            end_time=end_time,
            start_day=start_day,
            end_day=end_day,
            child_id=child_id
        )
        rotina.days_of_week.set(dias)
        rotina.save()
        return redirect(f"{request.path}?child_id={child_id}")
    else:
        dias_semana = Weekday.objects.all().order_by('day')
        children = Child.objects.filter(id__in=children_ids)
        selected_child = children.first() if children else None
        context = {'dias_semana': dias_semana, 'children': children, 'selected_child': selected_child}
        return render(request, 'rotina/rotinas.html', context)

def routine_details(request):
    det_rotina = Routine.objects.all()
    context = {
      'lista_rotinas': det_rotina
    }
    return render(request, 'rotina/rotina.html', context)

@csrf_exempt
@login_required
def excluir_rotina(request, rotina_id):
    if request.method == 'POST':
        Routine.objects.filter(id=rotina_id).delete()
    return redirect('rotina:rotina_hoje')

@csrf_exempt
@login_required
def alterar_rotina(request, rotina_id):
    rotina = get_object_or_404(Routine, id=rotina_id)
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if rotina.child_id not in children_ids:
        return redirect('rotina:rotina_hoje')
    if request.method == 'POST':
        rotina.description = request.POST.get('description')
        rotina.start_time = request.POST.get('start_time')
        rotina.end_time = request.POST.get('end_time')
        rotina.start_day = request.POST.get('start_day')
        rotina.end_day = request.POST.get('end_day') or None
        dias = request.POST.getlist('days_of_week')
        rotina.days_of_week.set(dias)
        rotina.save()
        return redirect(f"{request.path}?child_id={rotina.child_id}")
    dias_semana = Weekday.objects.all().order_by('day')
    children = Child.objects.filter(id__in=children_ids)
    context = {'rotina': rotina, 'dias_semana': dias_semana, 'children': children, 'selected_child': rotina.child}
    return render(request, 'rotina/rotinas.html', context)