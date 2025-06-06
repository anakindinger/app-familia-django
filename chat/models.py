from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Child

class Message(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}..."
