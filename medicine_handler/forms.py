from django import forms 
from .models import Person

from django.utils.translation import gettext_lazy as _
#from ckeditor.widgets import CKEeditorWidget 

class PersonForm(forms.Form):
    class meta:
        model = Person
        fields = '__all__'