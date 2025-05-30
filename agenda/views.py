from django.shortcuts import render, get_object_or_404
from .models import Evento
import calendar
from datetime import date
from django.contrib.auth.decorators import login_required
from usuario.models import UsuarioChild
from dashboard.models import Child

# Create your views here.
@login_required
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

    # Filtra apenas as crianças do usuário
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    children = Child.objects.filter(id__in=children_ids)
    child_id = request.GET.get('child_id')
    if child_id and int(child_id) in children_ids:
        selected_child = get_object_or_404(Child, id=child_id)
    else:
        selected_child = children.first() if children else None
        child_id = selected_child.id if selected_child else None
    # Filtra eventos da criança selecionada
    eventos = Evento.objects.filter(child_id=child_id, date__month=mes, date__year=ano) if child_id else []

    today = date.today()
    weekday_map = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7'}
    weekday_str = weekday_map[today.weekday()]
    tomorrow = (today.weekday() + 1) % 7
    weekday_tmr = weekday_map[tomorrow]

    context = {
        'mes_atual': mes,
        'ano_atual': ano,
        'anos': anos,
        'semanas': semanas,
        'meses': meses,
        'lista_eventos': eventos,
        'children': children,
        'selected_child': selected_child,
        'weekday_str': weekday_str,
        'weekday_tmr': weekday_tmr,
    }
    return render(request, 'agenda/calendario.html', context)
