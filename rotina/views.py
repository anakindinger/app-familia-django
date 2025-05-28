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
    weekday_map = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '1'}
    weekday_str = weekday_map[today.weekday()]
    # Filtra rotinas que contenham o dia de hoje (ManyToMany)
    routine_today = Routine.objects.all()
    context = {
        'rotina_hoje': routine_today,
        'data_atual': today,
    }
    return render(request, 'rotina/list_routines.html', context)