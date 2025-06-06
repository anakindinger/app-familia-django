from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:child_id>/', views.chat_view, name='chat'),
    path('<int:child_id>/messages/', views.chat_messages_json, name='chat_messages_json'),
]
