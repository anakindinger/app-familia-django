from django.shortcuts import render
from .models import Evento
from django.template import loader

# Create your views here.
def index(request):
    lista_eventos = Evento.objects.order_by('date')
    template = loader.get_template('agenda/calendario.html')
    context = {
        'lista_eventos': lista_eventos,
    }
    return render(request, 'agenda/calendario.html', context)
