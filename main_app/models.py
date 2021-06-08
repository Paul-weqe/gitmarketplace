from django.contrib.auth.models import User
from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"Repository <username: {self.user.username} - name: {self.name}>")
