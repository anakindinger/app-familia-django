from django.urls import path
from . import views

app_name = 'rotina'

urlpatterns = [
    path('', views.list_routines, name='list_routines'),
    
]