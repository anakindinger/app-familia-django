from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar/', views.cadastrar_evento, name='cadastrar_evento'),
    path('excluir/<int:evento_id>/', views.excluir_evento, name='excluir_evento'),
    path('alterar/<int:evento_id>/', views.alterar_evento, name='alterar_evento'),
    path('aprovar_evento/<int:evento_id>/', views.aprovar_evento, name='aprovar_evento'),
]