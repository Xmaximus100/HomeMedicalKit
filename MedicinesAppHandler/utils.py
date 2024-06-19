import csv
from .models import MedicineName

def import_medicine_names_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0].strip()  # zakładamy, że nazwa leku jest w pierwszej kolumnie
            if name:
                MedicineName.objects.get_or_create(name=name)