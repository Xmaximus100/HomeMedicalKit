from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    firstname = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username


class MedicineName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(MedicineName, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.quantity}) - Expires on {self.expiration_date}'


class SideEffect(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description


class Substance(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

