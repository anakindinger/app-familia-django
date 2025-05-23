from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Child, School, Health

def index(request):
    lista_criancas = Child.objects.order_by('name')
    template = loader.get_template('dashboard/index.html')
    context = {
        'lista_criancas': lista_criancas,
    }
    return render(request, 'dashboard/index.html', context)
# Create your views here.

def child_list(request, child_id):
    response = "Voê está visualizando a lista de crianças com id %s."
    return HttpResponse(response % child_id)

'''def child_detail(request, child_id):
    child = Child.objects.get(pk=child_id)
    school = School.objects.filter(child=child)
    health = Health.objects.filter(child=child)
    return render(request, 'dashboard/child_detail.html', {'child': child, 'school': school, 'health': health})'''