from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import User, Medicine, SideEffect, Substance, MedicineName
from .forms import SignUpForm, LoginForm, MedicineForm, SideEffectForm, SubstanceForm, SearchForm, RecordsPerPageForm
from .utils import import_medicine_names_from_csv
import matplotlib.pyplot as plt
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
import base64


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
            return redirect('home')
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
                return redirect('home')
            else:
                messages.error(request, 'Nieprawidłowy email lub hasło.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'home.html')


@login_required
def medicines_names_list(request):
    search_form = SearchForm(request.GET)
    records_form = RecordsPerPageForm(request.GET)
    medicines = MedicineName.objects.all()

    # Obsługa formularza wyszukiwania
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword', 10)
        if keyword:
            medicines = medicines.filter(
                Q(name__icontains=keyword)
            )

    # Obsługa formularza ustawiania liczby rekordów na stronie
    if records_form.is_valid():
        records_per_page = records_form.cleaned_data.get('records_per_page')
        if records_per_page:
            medicines = medicines[:records_per_page]

    return render(request, 'medicines_names_list.html', {
        'medicines': medicines,
        'search_form': search_form,
        'records_form': records_form,
    })


@login_required
def medicine_name_delete(request, medicine_id):
    medicine = MedicineName.objects.get(id=medicine_id)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicines_names_list')
    return render(request, 'medicine_name_confirm_delete.html', {'medicine': medicine})


@login_required
def import_medicines_names_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Musisz przesłać plik w formacie CSV.')
            return redirect('medicines_names_list')

        # Obsługa przesyłanego pliku CSV
        try:
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                name = row[0].strip()  # zakładamy, że nazwy leków są w pierwszej kolumnie
                if name:
                    MedicineName.objects.get_or_create(name=name)

            messages.success(request, 'Pomyślnie wczytano nazwy leków z pliku CSV.')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd podczas importowania danych: {str(e)}')

        return redirect('medicines_names_list')

    return render(request, 'import_medicines_names_from_csv.html')


@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(user=request.user)

    search_form = SearchForm(request.GET)
    records_form = RecordsPerPageForm(request.GET)
    results_per_page = request.GET.get('results_per_page', 10)  # domyślnie 10 wyników na stronie

    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        if keyword:
            # Filtrowanie po nazwie leku, nazwie substancji i efektach ubocznych
            medicines = medicines.filter(
                Q(name__name__icontains=keyword) |  # Filtr po nazwie leku
                Q(purpose__icontains=keyword) |  # Filtr po celu leku
                Q(substance__name__icontains=keyword) |  # Filtr po nazwie substancji
                Q(sideeffect__description__icontains=keyword)  # Filtr po opisie efektu ubocznego
            ).distinct()

    # Obsługa formularza ustawiania liczby rekordów na stronie
    if records_form.is_valid():
        records_per_page = records_form.cleaned_data.get('records_per_page')
        if records_per_page:
            medicines = medicines[:records_per_page]

    return render(request, 'medicines_list.html', {
        'medicines': medicines,
        'results_per_page': results_per_page,
        'search_form': search_form,
        'records_form': records_form,
    })


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
    writer.writerow(['Name', 'Purpose', 'Quantity', 'Expiration Date', 'Side Effects', 'Substances'])

    for medicine in medicines:
        side_effects = ', '.join([se.description for se in medicine.sideeffect_set.all()])
        substances = ', '.join([substance.name for substance in medicine.substance_set.all()])
        writer.writerow([
            medicine.name,
            medicine.purpose,
            medicine.quantity,
            medicine.expiration_date,
            side_effects,
            substances
        ])

    return response


@login_required
def side_effects_list(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    side_effects = medicine.sideeffect_set.all()

    # Obsługa formularza zmiany liczby wyników na stronie
    results_per_page = request.GET.get('results_per_page', 10)  # domyślnie 10 wyników na stronie
    paginator = Paginator(side_effects, results_per_page)

    page = request.GET.get('page')
    try:
        side_effects = paginator.page(page)
    except PageNotAnInteger:
        side_effects = paginator.page(1)
    except EmptyPage:
        side_effects = paginator.page(paginator.num_pages)

    return render(request, 'side_effects_list.html', {
        'medicine': medicine,
        'side_effects': side_effects,
        'results_per_page': results_per_page,
    })


@login_required
def add_side_effect(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = SideEffectForm(request.POST)
        if form.is_valid():
            side_effect = form.save(commit=False)
            side_effect.medicine = medicine
            side_effect.save()
            return redirect('medicine_detail', medicine_id=medicine.id)
    else:
        form = SideEffectForm()
    return render(request, 'add_side_effect.html', {'form': form, 'medicine': medicine})


@login_required
def delete_side_effect(request, side_effect_id):
    side_effect = get_object_or_404(SideEffect, id=side_effect_id)
    medicine_id = side_effect.medicine.id
    side_effect.delete()
    return redirect('medicine_detail', medicine_id=medicine_id)


@login_required
def side_effects_chart(request):
    medicines = Medicine.objects.filter(user=request.user)

    labels, counts = generate_side_effects_data(medicines)

    x = range(len(labels))

    plt.bar(x, counts, tick_label=labels)
    plt.xlabel('Leki')
    plt.ylabel('Liczba działań niepożądanych')
    plt.title('Wykres liczby działań niepożądanych dla każdego leku')
    plt.xticks(rotation=45)

    image_buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(image_buffer, format='png')
    plt.close()

    image_buffer.seek(0)
    image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    image_url = 'data:image/png;base64,' + image_data

    return render(request, 'side_effects_chart.html', {'image_url': image_url})


@login_required
def download_side_effects_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="side_effects_summary.pdf"'

    medicines = Medicine.objects.filter(user=request.user)
    labels, counts = generate_side_effects_data(medicines)

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 800, "Summary of Side Effects for All Medicines")

    pdf.setFont("Helvetica", 12)
    y = 750
    for label, count in zip(labels, counts):
        pdf.drawString(100, y, f"Medicine: {label}")
        y -= 20
        pdf.drawString(100, y, "Side Effects Count:")
        y -= 15
        pdf.drawString(120, y, f"{count}")
        y -= 20

    pdf.save()
    return response


def generate_side_effects_data(medicines):
    labels = []
    counts = []

    for medicine in medicines:
        side_effects_count = SideEffect.objects.filter(medicine=medicine).count()
        labels.append(medicine.name)
        counts.append(side_effects_count)

    return labels, counts


@login_required
def substances_list(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    substances = medicine.substance_set.all()

    # Obsługa formularza zmiany liczby wyników na stronie
    results_per_page = request.GET.get('results_per_page', 10)  # domyślnie 10 wyników na stronie
    paginator = Paginator(substances, results_per_page)

    page = request.GET.get('page')
    try:
        substances = paginator.page(page)
    except PageNotAnInteger:
        substances = paginator.page(1)
    except EmptyPage:
        substances = paginator.page(paginator.num_pages)

    return render(request, 'substances_list.html', {
        'medicine': medicine,
        'substances': substances,
        'results_per_page': results_per_page,
    })


@login_required
def add_substance(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = SubstanceForm(request.POST)
        if form.is_valid():
            substance = form.save(commit=False)
            substance.medicine = medicine
            substance.save()
            return redirect('medicine_detail', medicine_id=medicine.id)
    else:
        form = SubstanceForm()
    return render(request, 'add_substance.html', {'form': form, 'medicine': medicine})


@login_required
def delete_substance(request, substance_id):
    substance = get_object_or_404(Substance, id=substance_id)
    medicine_id = substance.medicine.id
    substance.delete()
    return redirect('medicine_detail', medicine_id=medicine_id)


@login_required
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'medicine_detail.html', {'medicine': medicine})