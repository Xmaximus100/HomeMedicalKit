from django import forms

from mediapp.models import Pacjent


class FormularzSzukajPacjenta(forms.Form):
    imie = forms.CharField(required=False)
    nazwisko = forms.CharField(required=False)
    data_ur = forms.DateField(required=False)
    waga_od = forms.IntegerField(min_value=0, max_value=300, required=False)
    waga_do = forms.IntegerField(min_value=0, max_value=300, required=False)


class FormularzPacjenta(forms.ModelForm):
    class Meta:
        model = Pacjent
        fields = "__all__"