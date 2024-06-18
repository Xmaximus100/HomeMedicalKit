import csv
from .models import MedicineName

def import_medicine_names_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[1].strip()  # zakładając, że nazwa leku jest w drugiej kolumnie
            if name:  # ignorujemy puste wiersze
                MedicineName.objects.get_or_create(name=name)