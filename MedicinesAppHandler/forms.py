from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Medicine, SideEffect, Substance
from django.forms.widgets import PasswordInput, TextInput


class SignUpForm(UserCreationForm):
    firstname = forms.CharField(max_length=100, required=False, help_text='Optional.')
    lastname = forms.CharField(max_length=100, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ['username', 'password1']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'purpose', 'quantity', 'expiration_date']


class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffect
        fields = ['description']


class SubstanceForm(forms.ModelForm):
    class Meta:
        model = Substance
        fields = ['name']