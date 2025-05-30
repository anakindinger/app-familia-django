from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UsuarioChild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey('dashboard.Child', on_delete=models.CASCADE, related_name='users')

    class Meta:
        unique_together = ('user', 'child')

    def __str__(self):
        return self.user.username +" - "+ self.child.name
