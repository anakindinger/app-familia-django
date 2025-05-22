from django.db import models

# Create your models here.
class Child(models.Model):
    name = models.CharField(max_length=100)
    dn = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    #school = models.ForeignKey('School', on_delete=models.CASCADE)
    #health = models.ForeignKey('Health', on_delete=models.CASCADE)

class School(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    classroom = models.CharField(max_length=10)
    teacher = models.CharField(max_length=100)

class Health(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    alergy = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    medication = models.CharField(max_length=100)