from django.shortcuts import render
from .models import Evento
import calendar
from datetime import date

# Create your views here.
def index(request):
    # Pega mês e ano da query string ou usa o atual
    mes = int(request.GET.get('mes', date.today().month))
    ano = int(request.GET.get('ano', date.today().year))

    # Gera matriz de semanas para o mês
    cal = calendar.Calendar(firstweekday=6)  # Domingo
    semanas = cal.monthdayscalendar(ano, mes)

    # Lista de anos para o select
    anos = list(range(date.today().year - 5, date.today().year + 6))

    # Lista de meses por extenso
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]

    context = {
        'mes_atual': mes,
        'ano_atual': ano,
        'anos': anos,
        'semanas': semanas,
        'meses': meses,
        'lista_eventos': Evento.objects.filter(date__year=ano, date__month=mes).order_by('date'),
    }
    return render(request, 'agenda/calendario.html', context)
