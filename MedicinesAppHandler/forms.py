from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Medicine, SideEffect, Substance

class SignUpForm(UserCreationForm):
    firstname = forms.CharField(max_length=100, required=True, help_text='First Name')
    lastname = forms.CharField(max_length=100, required=True, help_text='Last Name')
    email = forms.EmailField(max_length=200, required=True, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'email', 'password1', 'password2')

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