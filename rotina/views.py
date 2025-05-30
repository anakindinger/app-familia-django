from django.shortcuts import render, redirect
from .models import Routine, Weekday
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
'''def list_routines(request):
    context = {
        'lista_rotinas': Routine.objects.all().order_by('start_time'),
    }
    return render(request, 'rotina/list_routines.html', context)'''

@login_required
def rotina_hoje(request):
    today = date.today()
    weekday_map = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7'}
    weekday_str = weekday_map[today.weekday()]
    weekday_tmr = weekday_map[today.weekday()+1]
    routine_today = Routine.objects.filter(days_of_week__day=weekday_str).distinct().order_by('start_time')
    routine_tomorrow = Routine.objects.filter(days_of_week__day=weekday_tmr).distinct().order_by('start_time')
    dias_semana = Weekday.objects.all().order_by('day')
    todas_rotinas = Routine.objects.all().order_by('start_time')
    context = {
        'rotina_hoje': routine_today,
        'data_atual': today,
        'rotina_amanha': routine_tomorrow,
        'dias_semana': dias_semana,
        'todas_rotinas': todas_rotinas,
    }
    return render(request, 'rotina/rotinas.html', context)

@csrf_exempt
@login_required
def cadastrar_rotina(request):
    if request.method == 'POST':
        descricao = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        dias = request.POST.getlist('days_of_week')
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        rotina = Routine.objects.create(
            description=descricao,
            start_time=start_time,
            end_time=end_time,
            start_day=start_day,
            end_day=end_day
        )
        rotina.days_of_week.set(dias)
        rotina.save()
        return redirect('rotina:rotina_hoje')
    else:
        dias_semana = Weekday.objects.all().order_by('day')
        context = {'dias_semana': dias_semana}
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
    rotina = Routine.objects.get(id=rotina_id)
    if request.method == 'POST':
        rotina.description = request.POST.get('description')
        rotina.start_time = request.POST.get('start_time')
        rotina.end_time = request.POST.get('end_time')
        rotina.start_day = request.POST.get('start_day')
        rotina.end_day = request.POST.get('end_day') or None
        dias = request.POST.getlist('days_of_week')
        rotina.days_of_week.set(dias)
        rotina.save()
        return redirect('rotina:rotina_hoje')
    dias_semana = Weekday.objects.all().order_by('day')
    context = {'rotina': rotina, 'dias_semana': dias_semana}
    return render(request, 'rotina/rotinas.html', context)