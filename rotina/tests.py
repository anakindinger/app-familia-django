from django.test import TestCase, RequestFactory
from .models import Routine, Weekday
from .views import rotina_hoje
from datetime import time, date

class WeekdayModelTest(TestCase):
    def test_create_weekday(self):
        weekday = Weekday.objects.create(day='2')
        self.assertEqual(str(weekday), 'Monday')

    def test_invalid_weekday(self):
        with self.assertRaises(Exception):
            Weekday.objects.create(days_of_week='9')  # Não existe dia 9

class RoutineModelTest(TestCase):
    def setUp(self):
        self.monday = Weekday.objects.create(day='2')
        self.tuesday = Weekday.objects.create(day='3')

    def test_create_routine(self):
        routine = Routine.objects.create(description='Rotina Teste', start_time=time(8,0), end_time=time(9,0))
        routine.days_of_week.add(self.monday, self.tuesday)
        self.assertEqual(routine.days_of_week.count(), 2)
        self.assertEqual(str(routine), 'Rotina Teste')

    def test_routine_days_of_week(self):
        routine = Routine.objects.create(description='Outra Rotina', start_time=time(10,0), end_time=time(11,0))
        routine.days_of_week.add(self.monday)
        self.assertIn(self.monday, routine.days_of_week.all())

class RotinaHojeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Cria um Weekday para o dia da semana de hoje
        weekday = Weekday.objects.create(day=str((date.today().weekday() + 1) % 7 or 7))
        # Cria uma rotina para hoje
        self.routine = Routine.objects.create(description='Rotina Hoje', start_time=time(8,0), end_time=time(9,0))
        self.routine.days_of_week.add(weekday)

    def test_rotina_hoje_view(self):
        request = self.factory.get('/fake-url/')
        response = rotina_hoje(request)
        # Extrai o contexto do template usando response.context_data, se disponível, ou response.context, senão usa response.context_data, senão usa response.context_instance (para compatibilidade)
        context = response.context_data if hasattr(response, 'context_data') else getattr(response, 'context', None)
        if context is None and hasattr(response, 'context_instance'):
            context = response.context_instance
        # Se ainda não encontrou, tenta renderizar o template e pegar o contexto
        if context is None and hasattr(response, 'render'):
            response.render()
            context = response.context_data if hasattr(response, 'context_data') else getattr(response, 'context', None)
        # Se contexto não encontrado, falha o teste
        self.assertIsNotNone(context, 'Contexto não encontrado na resposta da view')
        rotina_hoje_context = context['rotina_hoje']
        rotina_hoje_list = list(rotina_hoje_context)
        self.assertIn(self.routine, rotina_hoje_list)
