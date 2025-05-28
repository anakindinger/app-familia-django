from django.urls import path
from . import views

app_name = 'rotina'

urlpatterns = [
    path('', views.rotina_hoje, name='rotina_hoje'),
    
]