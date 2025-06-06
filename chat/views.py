from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import Child
from .models import Message
from usuario.models import UsuarioChild
from django.utils import timezone
from django.http import JsonResponse
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key = os.getenv('API_KEY_SUA_API'))

instrucao = """
Você é um mediador de comunicação imparcial e objetivo.
Sua função é reformular as mensagens dos usuários para que elas se tornem declarações/perguntas impessoais, cordiais, sucintas e estritamente não-violentas.
Faça uso de linguagem simples.
Remova qualquer carga emocional (positiva ou negativa), julgamentos, acusações ou opiniões pessoais do usuário.
Foque exclusivamente em extrair e apresentar os fatos ou as necessidades da mensagem original.
Não responda a perguntas, não expresse opiniões e não adicione informações novas. Seu único objetivo é a reescrita neutra da comunicação do usuário.
"""
model = genai.GenerativeModel(
    'gemini-1.5-flash-8b',
    system_instruction=instrucao
)

def process_message_text(text,):
    try:
        response = model.generate_content(
            text
        )
        if response:
            return response.text
        else:
            return ["Não foi possível gerar opções para esta mensagem."]
    except Exception as e:
        return [f"Erro ao gerar resposta: {e}"]


@login_required
def chat_view(request, child_id):
    child = Child.objects.get(id=child_id)
    # Só responsáveis associados podem acessar
    if not UsuarioChild.objects.filter(user=request.user, child=child).exists():
        return redirect('dashboard:index')
    messages = Message.objects.filter(child=child).select_related('user').order_by('created_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            processed_text = process_message_text(text)
            Message.objects.create(child=child, user=request.user, text=processed_text, created_at=timezone.now())
            return redirect('chat:chat', child_id=child.id)
    return render(request, 'chat/chat.html', {'child': child, 'messages': messages})

@login_required
def chat_messages_json(request, child_id):
    child = Child.objects.get(id=child_id)
    if not UsuarioChild.objects.filter(user=request.user, child=child).exists():
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    messages = Message.objects.filter(child=child).select_related('user').order_by('created_at')
    data = [
        {
            'user': m.user.username,
            'text': m.text,
            'created_at': m.created_at.strftime('%d/%m/%Y %H:%M')
        } for m in messages
    ]
    return JsonResponse({'messages': data})
