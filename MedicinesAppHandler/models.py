from django.db import models


class Lekarz(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    specjalizacja = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.imie} {self.nazwisko} ({self.specjalizacja}) [{self.id}]'


class Pacjent(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    data_ur = models.DateField()
    waga = models.IntegerField()

    def __str__(self):
        return f'{self.imie} {self.nazwisko} ({self.data_ur.strftime("%Y-%m-%d")}) /{self.waga} kg/ [{self.id}]'


class Wizyta(models.Model):
    pacjent = models.ForeignKey(Pacjent, on_delete=models.PROTECT)
    lekarz = models.ForeignKey(Lekarz, on_delete=models.PROTECT)
    data = models.DateTimeField()

    def __str__(self):
        return f'{self.data.strftime("%Y-%m-%d")} (P: {self.pacjent_id}, L: {self.lekarz_id}) [{self.id}]'


class Recepta(models.Model):
    nazwa = models.CharField(max_length=200)
    wizyta = models.ForeignKey(Wizyta, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nazwa} (W: {self.wizyta_id}) [{self.id}]'

