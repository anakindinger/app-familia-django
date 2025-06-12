from django.db import models

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('aprovado', 'Aprovado'),
]

# Create your models here.
class Child(models.Model):
    name = models.CharField(max_length=100)
    dn = models.DateField("data de nascimento")
    height = models.DecimalField(decimal_places=2, max_digits=3)
    weight = models.DecimalField(decimal_places=3, max_digits=6)
    def __str__(self):
        return self.name

class School(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    classroom = models.CharField(max_length=10)
    teacher = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    def __str__(self):
        return self.child.name+ " - "+self.name + " - " + self.classroom

class Health(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    alergy = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    medication = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    def __str__(self):
        return self.child.name + " - " + self.alergy


