from django.db import models
from dashboard.models import Child

# Create your models here.
class Evento(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField("data")
    hour_init = models.TimeField("hora")
    hour_end = models.TimeField("hora")
    description = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.date} - {self.description}"