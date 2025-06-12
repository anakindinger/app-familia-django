from django.db import models
from dashboard.models import Child

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('aprovado', 'Aprovado'),
]

# Create your models here.
class Evento(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField("data")
    hour_init = models.TimeField("hora")
    hour_end = models.TimeField("hora")
    description = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    def __str__(self):
        return f"{self.date} - {self.description}"