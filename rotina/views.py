from django.shortcuts import render
from .models import Routine
from datetime import date

# Create your views here.
'''def list_routines(request):
    context = {
        'lista_rotinas': Routine.objects.all().order_by('start_time'),
    }
    return render(request, 'rotina/list_routines.html', context)'''

def rotina_hoje(request):
    today = date.today()
    # Django: weekday() -> segunda=0, domingo=6. Seu Weekday usa: domingo=1, segunda=2, ...
    weekday_map = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7'}
    weekday_str = weekday_map[today.weekday()]
    weekday_tmr = weekday_map[today.weekday()+1]
    # Filtra rotinas que contenham o dia de hoje (ManyToMany)
    routine_today = Routine.objects.filter(days_of_week__id=weekday_str).order_by('start_time')
    routine_tomorrow = Routine.objects.filter(days_of_week__id=weekday_tmr).order_by('start_time')
    context = {
        'rotina_hoje': routine_today,
        'data_atual': today,
        'rotina_amanha':routine_tomorrow,
    }
    return render(request, 'rotina/list_routines.html', context)