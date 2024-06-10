# inventory/tests.py

from django.test import TestCase
from .models import Item, Supplier

class InventoryTestCase(TestCase):
    def setUp(self):
        self.supplier1 = Supplier.objects.create(name="Supplier 1", contact_info="Contact Info 1")
        self.supplier2 = Supplier.objects.create(name="Supplier 2", contact_info="Contact Info 2")
        self.item1 = Item.objects.create(name="Item 1", description="Description 1", price=10.00)
        self.item2 = Item.objects.create(name="Item 2", description="Description 2", price=20.00)
        self.item1.suppliers.add(self.supplier1, self.supplier2)

    def test_item_creation(self):
        self.assertEqual(self.item1.name, "Item 1")
        self.assertEqual(self.item2.price, 20.00)

    def test_supplier_creation(self):
        self.assertEqual(self.supplier1.name, "Supplier 1")
        self.assertEqual(self.supplier2.contact_info, "Contact Info 2")

    def test_supply_relationship(self):
        self.assertEqual(self.item1.suppliers.count(), 2)
        self.assertEqual(self.supplier1.items.count(), 1)
