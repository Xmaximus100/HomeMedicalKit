from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    marks = models.CharField(max_length=100)

class Profile(models.Model):
    name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    marks = models.CharField(max_length=1000)
    age = models.PositiveIntegerField()

class ToDo(models.Model):
    task = models.TextField()
    completed = models.BooleanField(default=False)
