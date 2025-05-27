from django.shortcuts import render
from .models import Routine
from datetime import date

# Create your views here.
def list_routines(request):
    context = {
        'lista_rotinas': Routine.objects.all().order_by('start_time'),
    }
    return render(request, 'rotina/list_routines.html', context)

def rotina_hoje(request):
    today = date.today()
    routine_today = Routine.objects.filter(days_of_week__day=today.weekday()).order_by('start_time')
    if not routine_today:
        routine_today = Routine.objects.none()
    
    context = {
        'rotina_hoje': routine_today,
        'data_atual': today,
    }
    return render(request, 'rotina/list_routines.html', context)