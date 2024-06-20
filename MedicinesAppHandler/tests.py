from django.test import TestCase

# Create your tests here.
import tempfile
import csv
from django.test import TestCase, Client
from django.urls import reverse
from .models import Medicine, Substance, SideEffect, User

class MedicineModelTest(TestCase):

    def setUp(self):
        self.substance = Substance.objects.create(name="Paracetamol", description="Pain reliever")
        self.medicine = Medicine.objects.create(
            name="Tylenol",
            expiration_date="2023-12-31",
            quantity=10,
            substance=self.substance
        )

    def test_medicine_creation(self):
        self.assertEqual(self.medicine.name, "Tylenol")
        self.assertEqual(self.medicine.substance.name, "Paracetamol")

    def test_medicine_str(self):
        self.assertEqual(str(self.medicine), "Tylenol")

class SubstanceModelTest(TestCase):

    def setUp(self):
        self.substance = Substance.objects.create(name="Ibuprofen", description="Anti-inflammatory")

    def test_substance_creation(self):
        self.assertEqual(self.substance.name, "Ibuprofen")

    def test_substance_str(self):
        self.assertEqual(str(self.substance), "Ibuprofen")

class SideEffectModelTest(TestCase):

    def setUp(self):
        self.side_effect = SideEffect.objects.create(name="Nausea", description="Feeling of sickness")

    def test_side_effect_creation(self):
        self.assertEqual(self.side_effect.name, "Nausea")

    def test_side_effect_str(self):
        self.assertEqual(str(self.side_effect), "Nausea")

class UserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

class MedicineViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.substance = Substance.objects.create(name="Paracetamol", description="Pain reliever")
        self.medicine = Medicine.objects.create(
            name="Tylenol",
            expiration_date="2023-12-31",
            quantity=10,
            substance=self.substance
        )

    def test_medicine_list_view(self):
        response = self.client.get(reverse('medicine_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tylenol")

    def test_medicine_add_view(self):
        response = self.client.post(reverse('medicine_add'), {
            'name': 'Aspirin',
            'expiration_date': '2024-01-01',
            'quantity': 20,
            'substance': self.substance.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Medicine.objects.last().name, 'Aspirin')

    def test_medicine_edit_view(self):
        response = self.client.post(reverse('medicine_edit', args=[self.medicine.id]), {
            'name': 'Tylenol Extra',
            'expiration_date': '2023-12-31',
            'quantity': 10,
            'substance': self.substance.id
        })
        self.assertEqual(response.status_code, 302)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.name, 'Tylenol Extra')

    def test_medicine_delete_view(self):
        response = self.client.post(reverse('medicine_delete', args=[self.medicine.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Medicine.objects.filter(id=self.medicine.id).count(), 0)

class CSVImportExportTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_import_medicines_names_from_csv(self):
        csv_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['name'])
        writer.writerow(['Aspirin'])
        writer.writerow(['Ibuprofen'])
        csv_file.close()

        with open(csv_file.name, 'rb') as f:
            response = self.client.post(reverse('import_medicines_names_from_csv'), {'csv_file': f})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Medicine.objects.count(), 2)

    def test_export_medicines_csv(self):
        substance = Substance.objects.create(name="Paracetamol", description="Pain reliever")
        Medicine.objects.create(name="Tylenol", expiration_date="2023-12-31", quantity=10, substance=substance)

        response = self.client.get(reverse('export_medicines_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Tylenol', content)

