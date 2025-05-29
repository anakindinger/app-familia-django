from django.db import models
from datetime import date


class Routine(models.Model):
    description = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.ManyToManyField('Weekday', related_name='routines', help_text='Dias da semana em que a rotina se aplica.')
    start_day = models.DateField(default=date.today)
    end_day = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.description

class Weekday(models.Model):
    WEEK_DAYS = [
            ('1','SEG'),
            ('2','TER'),
            ('3','QUA'),
            ('4','QUI'),
            ('5','SEX'),
            ('6','SAB'),
            ('7','DOM')
        ]
    day = models.CharField(choices=WEEK_DAYS, max_length=3, unique=True, help_text='Dia da semana para a rotina.')
    def __str__(self):
        return dict(self.WEEK_DAYS).get(self.day, self.day)
    