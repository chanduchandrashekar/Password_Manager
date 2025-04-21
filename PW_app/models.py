from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    masterkey = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class SavedPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.CharField(max_length=100)
    username=models.CharField(max_length=100,default="default_username")
    password = models.CharField(max_length=300)  # Encrypted passwordpython m

    def __str__(self):
        return f"{self.site} - {self.user.username}"
