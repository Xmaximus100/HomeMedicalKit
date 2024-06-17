from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import Person, Profile, ToDo, Medicine, MedicineName, SideEffect, Substance
# from .forms import PostForm
from .forms import SignUpForm, LoginForm, MedicineForm, SideEffectForm, SubstanceForm
from tablib import Dataset
from .resources import PersonResource
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import csv

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

def start_view(request):
    return render(request, 'start.html')

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')  # lub jakakolwiek inna strona po zalogowaniu
        else:
            messages.error(request, "Nieprawidłowy email lub hasło.")
    return render(request, 'login.html', context={'loginform':form})

def logout_view(request):
    logout(request)
    return redirect('login')  # lub jakakolwiek inna strona po wylogowaniu

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.refresh_from_db()  # Load the profile instance created by the signal
                user.firstname = form.cleaned_data.get('firstname')
                user.lastname = form.cleaned_data.get('lastname')
                user.email = form.cleaned_data.get('email')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.email, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Konto zostało utworzone pomyślnie!')
                    return redirect('login')
                else:
                    messages.error(request, 'Wystąpił problem podczas logowania. Spróbuj ponownie.')
            except NameError:
                messages.error(request, f'Wystąpił problem {NameError} podczas logowania. Spróbuj ponownie.')
        else:
            messages.error(request, 'Nieprawidłowe dane formularza. Spróbuj ponownie.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', context={'form': form})


def home_view(request):
    return render(request, 'home.html')


@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(user=request.user)
    return render(request, 'medicines/list.html', {'medicines': medicines})


@login_required
def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            medicine.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicines/form.html', {'form': form})


@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'medicines/form.html', {'form': form})


@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicines/confirm_delete.html', {'medicine': medicine})


@login_required
def export_medicines_csv(request):
    medicines = Medicine.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medicines.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Purpose', 'Quantity', 'Expiration Date'])
    for medicine in medicines:
        writer.writerow([medicine.name, medicine.purpose, medicine.quantity, medicine.expiration_date])
    return response


@login_required
def side_effects_chart(request):
    medicines = Medicine.objects.filter(user=request.user)
    side_effects_count = {medicine.name.name: medicine.sideeffect_set.count() for medicine in medicines}

    plt.bar(side_effects_count.keys(), side_effects_count.values())
    plt.xlabel('Medicines')
    plt.ylabel('Number of Side Effects')
    plt.title('Number of Side Effects for Each Medicine')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='side_effects_chart.pdf')