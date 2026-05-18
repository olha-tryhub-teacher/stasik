from django.test import TestCase
from .models import Manufacturer

class ManufacturerModelTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(title='Django для профі', phone_number='88005553535', addres='вул.12 а')

    def test_string_representation(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), 'Django для профі')