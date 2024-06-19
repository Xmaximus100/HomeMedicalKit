import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from MedicinesAppHandler.models import User, Medicine, SideEffect, Substance, MedicineName

class Command(BaseCommand):
    help = 'Generates sample data for Medicines, SideEffects, Substances, and MedicineNames'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating sample data...')

        # Lista nazw leków
        medicine_names_list = [
            "Alphexa", "Brionex", "Calypral", "Dolevir", "Elystra", "Fomadin", "Gerotrin", "Hyplorin",
            "Iradex", "Juvexin", "Kaldorin", "Lexotan", "Meflorin", "Nelcoral", "Omipax", "Poltracin",
            "Quintril", "Remcorta", "Salyprid", "Talrivin", "Ulcoten", "Valcora", "Wintrixa", "Xalorin",
            "Yondrex", "Zolaprin", "Altexin", "Brevoxil", "Cyclopar", "Dynaflex", "Elotrin", "Florazol",
            "Glycotec", "Halipran", "Imunol", "Juvetra", "Kintrex", "Lorizan", "Myotril", "Nextril",
            "Oxyvex", "Pyralgin", "Quintex", "Relotrin", "Synapro", "Telforin", "Uroplex", "Velotrin",
            "Xyloprim", "Zytrafin", "Alproxan", "Bytrixin", "Clavitra", "Deltavir", "Eprosor", "Flynterol",
            "Gylorin", "Haplexa", "Ibunex", "Juvecor", "Klyntral", "Lymphex", "Melotril", "Netralex",
            "Optivax", "Palorin", "Quinotex", "Reglorin", "Syntoril", "Teloprox", "Ultranex", "Valtran",
            "Wintrex", "Xyntexa", "Zyloxin", "Ampritin", "Bactrol", "Cloroxal", "Delphrin", "Eriprax",
            "Flextor", "Gravetol", "Hepatrix", "Invexor", "Jextrin", "Kolaflex", "Lortavin", "Myxotran",
            "Nyvalin", "Omniflex", "Pyratex", "Quroxal", "Resotrin", "Syntrel", "Tolrex", "Uriprax",
            "Valtrexin", "Xenoprin", "Zyletin", "Ablovex"
        ]

        # Lista substancji
        substances_list = [
            "Paracetamol", "Ibuprofen", "Aspiryna", "Amoksycylina", "Ceftriakson", "Deksametazon",
            "Prednizon", "Kodeina", "Morfina", "Tramadol", "Loperamid", "Omeprazol", "Pantoprazol",
            "Simwastatyna", "Atorwastatyna", "Metoprolol", "Bisoprolol", "Losartan", "Walsartan",
            "Enalapryl", "Ramipryl", "Hydrochlorotiazyd", "Furosemid", "Spironolakton", "Metformina",
            "Insulina", "Glibenklamid", "Gliklazyd", "Diklofenak", "Ketoprofen", "Naproksen",
            "Klarytromycyna", "Erytromycyna", "Azitromycyna", "Ciprofloxacyna", "Lewofloxacyna",
            "Amikacyna", "Gentamycyna", "Wankomycyna", "Chloramfenikol", "Doxycyklina", "Tetracyklina",
            "Fluoksetyna", "Sertralina", "Paroksetyna", "Citalopram", "Escitalopram", "Amitryptylina",
            "Nortryptylina", "Wenlafaksyna", "Duloksetyna", "Pregabalina", "Gabapentyna", "Karbamazepina",
            "Walproinian", "Lamotrygina", "Fenobarbital", "Diazepam", "Alprazolam", "Lorazepam",
            "Zolpidem", "Melatonina", "Warfaryna", "Acenokumarol", "Enoksaparyna", "Klopidogrel",
            "Tiklopidyna", "Kwas acetylosalicylowy", "Heparyna", "Metoklopramid", "Ondansetron",
            "Loperamid", "Drotaweryna", "Butylobromek hioscyny", "Dekstrometorfan", "Fenylefryna",
            "Pseudoefedryna", "Klemastyna", "Loratadyna", "Ceteryzyna", "Feksofenadyna", "Montelukast",
            "Flutikazon", "Budezonid", "Salbutamol", "Formoterol", "Tiotropium", "Bromek ipratropium",
            "Oksykodon", "Tapentadol", "Metadon", "Buprenorfina", "Nalokson", "Naltrekson", "Lidokaina",
            "Prokaina", "Bupiwakaina", "Chlorheksydyna"
        ]

        # Lista działań niepożądanych
        side_effects_list = [
            "Bóle głowy", "Nudności", "Biegunka", "Zawroty głowy", "Senność", "Bezsenność",
            "Wysypka", "Świąd skóry", "Suchość w ustach", "Zmęczenie", "Zaburzenia żołądkowo-jelitowe",
            "Bóle mięśniowe", "Zmiany nastroju", "Zmniejszenie apetytu", "Wzrost ciśnienia krwi",
            "Spadek ciśnienia krwi", "Problemy z pamięcią", "Problemy z koncentracją",
            "Problemy z równowagą", "Zmiany wagi ciała", "Zmiany w rytmie serca", "Wzrost cholesterolu",
            "Zaburzenia smaku", "Zaburzenia wzroku", "Zaburzenia słuchu", "Problemy z oddychaniem",
            "Zaburzenia wątroby", "Zaburzenia nerek", "Obrzęki", "Zmiany hormonalne",
            "Alergiczne reakcje skórne", "Problemy z trawieniem", "Problemy z układem nerwowym",
            "Problemy z układem krążenia", "Problemy z układem oddechowym", "Problemy z układem pokarmowym",
            "Problemy z układem moczowym", "Problemy z układem immunologicznym", "Problemy z układem hormonalnym",
            "Problemy z układem rozrodczym", "Problemy z układem kostno-stawowym", "Problemy z układem krwiotwórczym",
            "Problemy z układem limfatycznym"
        ]

        # Upewnij się, że jest przynajmniej jeden użytkownik
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR('No users found in the database.'))
            return

        # Generowanie nazw leków
        medicine_names = []
        for name in medicine_names_list:
            medicine_name = MedicineName.objects.create(name=name)
            medicine_names.append(medicine_name)

        # Generowanie leków
        for _ in range(50):
            medicine = Medicine.objects.create(
                user=User.objects.first(),  # Użyj pierwszego użytkownika
                name=random.choice(medicine_names),  # Wybierz losową nazwę leku
                purpose='Example purpose',
                quantity=random.randint(1, 100),
                expiration_date=datetime.now() + timedelta(days=random.randint(1, 365)),
            )

            # Generowanie skutków ubocznych
            for _ in range(random.randint(1, 20)):
                SideEffect.objects.create(
                    medicine=medicine,
                    description=random.choice(side_effects_list),
                )

            # Generowanie substancji
            for _ in range(random.randint(1, 5)):
                Substance.objects.create(
                    medicine=medicine,
                    name=random.choice(substances_list),
                )

        self.stdout.write(self.style.SUCCESS('Sample data generated successfully!'))