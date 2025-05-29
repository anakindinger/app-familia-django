from django.urls import path
from . import views

app_name = 'rotina'

urlpatterns = [
    path('', views.rotina_hoje, name='rotina_hoje'),
    path('cadastrar/', views.cadastrar_rotina, name='cadastrar_rotina'),
    path('excluir/<int:rotina_id>/', views.excluir_rotina, name='excluir_rotina'),
    path('alterar/<int:rotina_id>/', views.alterar_rotina, name='alterar_rotina'),
]