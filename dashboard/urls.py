from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:child_id>/', views.child_list, name='child_list'),
    path('cadastrar/', views.cadastrar_child, name='cadastrar_child'),
    path('associar-usuario/<int:child_id>/', views.associar_usuario_child, name='associar_usuario_child'),
    path('aprovar_school/<int:school_id>/', views.aprovar_school, name='aprovar_school'),
    path('aprovar_health/<int:health_id>/', views.aprovar_health, name='aprovar_health'),
    path('recados/', views.recados, name='recados'),
]