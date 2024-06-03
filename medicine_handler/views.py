from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages, auth
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Person, Profile, ToDo
# from .forms import PostForm
from tablib import Dataset
from .resources import PersonResource

# Create your views here.
def home(request):
    return render(request, 'home.html')

def todos(request):
    items = ToDo.objects.all()
    return render(request, "todos.html", {"todos": items})

def index(request):
    labels = []
    data =[]

    queryset = Profile.objects.order_by('-age')[:5]
    for person in queryset:
        labels.append(person.name)
        data.append(person.age)
    return render(request, 'index.html', {
        'labels':labels,
        'data': data
    })

def importExcel(request):
    if request.method == "POST":
        oerson_resource = PersonResource()
        dataset = Dataset()
        new_person = request.FILES['my_file']
        imported_data = dataset.load(new_person.read(), format='xlsx')
        for data in imported_data:
            value = Person(
                data[0],
                data[1],
                data[2]
            )
            value.save()

    return render(request, 'form.html')

def say_hello(request):
    x = 10
    y = 2
    return render(request, 'main_page.html') #{'name': 'Admin'}
