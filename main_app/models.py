from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=150)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)