from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class MedicineName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Example default value, adjust as needed
    name = models.ForeignKey(MedicineName, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.quantity}) - Expires on {self.expiration_date}'

    def add_side_effect(self, description):
        side_effect = SideEffect(medicine=self, description=description)
        side_effect.save()

    def remove_side_effect(self, side_effect_id):
        side_effect = SideEffect.objects.get(id=side_effect_id, medicine=self)
        side_effect.delete()

    def update_side_effect(self, side_effect_id, description):
        side_effect = SideEffect.objects.get(id=side_effect_id, medicine=self)
        side_effect.description = description
        side_effect.save()

    def add_substance(self, name):
        substance = Substance(medicine=self, name=name)
        substance.save()

    def remove_substance(self, substance_id):
        substance = Substance.objects.get(id=substance_id, medicine=self)
        substance.delete()

    def update_substance(self, substance_id, name):
        substance = Substance.objects.get(id=substance_id, medicine=self)
        substance.name = name
        substance.save()


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

