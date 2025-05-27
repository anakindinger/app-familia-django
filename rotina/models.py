from django.db import models


class Routine(models.Model):
    description = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.ManyToManyField('Weekday', related_name='routines', help_text='Dias da semana em que a rotina se aplica.')
    def __str__(self):
        return self.description

class Weekday(models.Model):
    WEEK_DAYS = [
            ('2','Monday'),
            ('3','Tuesday'),
            ('4','Wednesday'),
            ('5','Thursday'),
            ('6','Friday'),
            ('7','Saturday'),
            ('1','Sunday')
        ]
    day = models.CharField(choices=WEEK_DAYS, max_length=3, unique=True, help_text='Dia da semana para a rotina.')
    def __str__(self):
        return dict(self.WEEK_DAYS).get(self.day, self.day)
    