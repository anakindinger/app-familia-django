from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
import calendar
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from usuario.models import UsuarioChild
from dashboard.models import Child
from dashboard.views import get_child_context

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
        'weekday_str': weekday_str,
        'weekday_tmr': weekday_tmr,
    }
    context.update(get_child_context(request))
    return render(request, 'agenda/calendario.html', context)

@csrf_exempt
@login_required
def cadastrar_evento(request):
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if request.method == 'POST':
        descricao = request.POST.get('description')
        hour_init = request.POST.get('hour_init')
        hour_end = request.POST.get('hour_end')
        date = request.POST.getlist('date')
        child_id = request.POST.get('child_id')
        if not child_id or int(child_id) not in children_ids:
            return redirect('agenda:index')
        evento = Evento.objects.create(
            description=descricao,
            date=date,
            hour_init=hour_init,
            hour_end=hour_end,
            child_id=child_id
        )
        
        evento.save()
        return redirect(f"{request.path}?child_id={child_id}")
    else:
        children = Child.objects.filter(id__in=children_ids)
        selected_child = children.first() if children else None
        context = {'children': children, 'selected_child': selected_child}
        return render(request, 'agenda/calendario.html', context)


@csrf_exempt
@login_required
def excluir_evento(request, evento_id):
    if request.method == 'POST':
        Evento.objects.filter(id=evento_id).delete()
    return redirect('agenda:index')

@csrf_exempt
@login_required
def alterar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    children_ids = UsuarioChild.objects.filter(user=request.user).values_list('child_id', flat=True)
    if evento.child_id not in children_ids:
        return redirect('evento:index')
    if request.method == 'POST':
        evento.descricao = request.POST.get('description')
        evento.hour_init = request.POST.get('hour_init')
        evento.hour_end = request.POST.get('hour_end')
        evento.date = request.POST.getlist('date')
        evento.save()
        return redirect(f"{request.path}?child_id={evento.child_id}")
  
    children = Child.objects.filter(id__in=children_ids)
    context = {'evento': evento, 'children': children, 'selected_child': evento.child}
    return render(request, 'agenda/calendario.html', context)