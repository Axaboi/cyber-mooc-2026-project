
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class Input(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    secret_answer_text = models.CharField(max_length=200)