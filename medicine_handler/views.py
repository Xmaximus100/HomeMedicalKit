from django.shortcuts import render, redirect
import datetime
from django.db.models import Sum
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Person, Profile, ToDo, Medicine, MedicineName, SideEffect, Substance
# from .forms import PostForm
from .forms import SignUpForm, LoginForm, MedicineForm, SideEffectForm, SubstanceForm
from tablib import Dataset
from .resources import PersonResource
from reportlab.pdfgen import canvas
from .utils import import_medicine_names_from_csv
import matplotlib.pyplot as plt
import csv
import io

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

def file_upload_view(request):
    print(request.FILES)
    return render(request, 'import_excel.html')
 
def importExcel(request):
    if request.method == "POST":
        person_resource = PersonResource()
        dataset = Dataset()
        try:
            new_person = request.FILES['my_file']
            imported_data = dataset.load(new_person.read(), format='xlsx')
            for data in imported_data:
                value = Person(
                    data[0],
                    data[1],
                    data[2]
                )
                value.save()
                messages.success(request, 'Dane zostały wgrane pomyślnie!')
        except:
            messages.error(request, f'Nieprawidłowe dane. Spróbuj ponownie.')

    return render(request, 'import_excel.html')

def say_hello(request):
    x = 10
    y = 2
    return render(request, 'main_page.html') #{'name': 'Admin'}

def start_view(request):
    return render(request, 'start.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Konto zostało utworzone pomyślnie!')
            return redirect('home')  # Przekierowanie na stronę po zalogowaniu
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Przekierowanie na stronę po zalogowaniu
            else:
                messages.error(request, 'Nieprawidłowy email lub hasło.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Przekierowanie na stronę logowania po wylogowaniu


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required
def import_medicines_from_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            import_medicine_names_from_csv(csv_file)
            messages.success(request, 'Rekordy zostały pomyślnie zaimportowane do bazy danych.')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd podczas importowania rekordów: {str(e)}')
    return render(request, 'import_medicines.html')


@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(user=request.user)

    # Pobierz liczbę wyników na stronie z parametru GET (jeśli dostępny)
    results_per_page = request.GET.get('results_per_page', 10)  # domyślnie 10 wyników na stronie
    paginator = Paginator(medicines, results_per_page)

    page = request.GET.get('page')
    try:
        medicines = paginator.page(page)
    except PageNotAnInteger:
        medicines = paginator.page(1)
    except EmptyPage:
        medicines = paginator.page(paginator.num_pages)

    return render(request, 'medicines_list.html', {'medicines': medicines, 'results_per_page': results_per_page})


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
    return render(request, 'medicines_form.html', {'form': form})


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
    return render(request, 'medicines_form.html', {'form': form})


@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, user=request.user)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicines_confirm_delete.html', {'medicine': medicine})


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
def side_effects_list(request):
    side_effects = SideEffect.objects.filter(medicine__user=request.user)

    # Pobierz liczbę wyników na stronie z parametru GET (jeśli dostępny)
    results_per_page = request.GET.get('results_per_page', 10)  # domyślnie 10 wyników na stronie
    paginator = Paginator(side_effects, results_per_page)

    page = request.GET.get('page')
    try:
        side_effects = paginator.page(page)
    except PageNotAnInteger:
        side_effects = paginator.page(1)
    except EmptyPage:
        side_effects = paginator.page(paginator.num_pages)

    return render(request, 'side_effects_list.html',{'side_effects': side_effects, 'results_per_page': results_per_page})


@login_required
def side_effects_chart(request):
    medicines = Medicine.objects.filter(user=request.user)
    side_effects_count = {medicine.name: medicine.sideeffect_set.count() for medicine in medicines}

    plt.bar(side_effects_count.keys(), side_effects_count.values())
    plt.xlabel('Medicines')
    plt.ylabel('Number of Side Effects')
    plt.title('Number of Side Effects for Each Medicine')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='side_effects_chart.png')