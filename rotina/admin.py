from django.contrib import admin
from .models import Routine, Weekday
# Register your models here.

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('description', 'child', 'start_time', 'end_time')

admin.site.register(Weekday)