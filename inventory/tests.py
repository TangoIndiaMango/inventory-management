import copy
from rest_framework.test import APIClient
from django.test import TestCase
from .models import Item, Supplier


class InventoryTestCase(TestCase):
    def setUp(self):
        self.supplier1 = Supplier.objects.create(
            name="Tango User", contact_info="+1 233 6798"
        )
        self.supplier2 = Supplier.objects.create(
            name="Fisher Admin", contact_info="+9 348 99234"
        )
        self.item1 = Item.objects.create(
            name="Sony HeadPhones",
            description="These are the type of headphones used in the late 80's",
            price=10.00,
        )
        self.item2 = Item.objects.create(
            name="Nike Sneakers",
            description="Feel the high power of bouncing shoes, flee to survive",
            price=20.00,
        )
        self.supplier1.items.add(self.item1)
        self.supplier1.items.add(self.item2)
        self.supplier2.items.add(self.item2)
        self.client = APIClient()

    def test_item_creation(self):
        self.assertEqual(self.item1.name, "Sony HeadPhones")
        self.assertEqual(self.item2.price, 20.00)

    def test_supplier_creation(self):
        self.assertEqual(self.supplier1.name, "Tango User")
        self.assertEqual(self.supplier2.contact_info, "+9 348 99234")

    def test_supplier_item_relationship(self):
        self.assertEqual(self.supplier1.items.count(), 2)
        self.assertEqual(self.supplier2.items.count(), 1)

    def test_get_suppliers(self):
        response = self.client.get("/api/inventory/suppliers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_post_supplier(self):
        data = {
            "name": "New Supplier",
            "contact_info": "+1 234 906 789",
            "items": [
                {
                    "name": "Monitor LCD curved",
                    "description": "This item is a valuable cross road enterprise data insence",
                    "price": "120.99",
                },
                {
                    "name": "Pangea Cup",
                    "description": "This item is a valuable cross road enterprise data insence",
                    "price": "1120.99",
                },
            ],
        }

        response = self.client.post("/api/inventory/suppliers", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Supplier.objects.count(), 3)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.count(), 4)

    def test_get_one_supplier(self):
        response = self.client.get(f"/api/inventory/suppliers/{self.supplier1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Tango User")
        self.assertEqual(len(response.data["items"]), 2)

    def test_delete_supplier(self):
        response = self.client.delete(
            f"/api/inventory/suppliers/{self.supplier1.id}", format="json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 2)

    def test_add_existing_item_to_supplier(self):
        data = {
            "name": "New Supplier",
            "contact_info": "Contact Info",
            "items": [self.item1.id, self.item2.id],
        }

        mutable_data = copy.deepcopy(data)

        response = self.client.post(
            "/api/inventory/suppliers", mutable_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Supplier.objects.count(), 3)
        self.assertEqual(Item.objects.count(), 2)

    def test_add_new_and_existing_items_to_supplier(self):
        data = {
            "name": "New Supplier",
            "contact_info": "Contact Info",
            "items": [
                {"name": "New Item 1", "description": "Description 1", "price": 100.00},
                self.item1.id,
            ],
        }

        mutable_data = copy.deepcopy(data)

        response = self.client.post(
            "/api/inventory/suppliers", mutable_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Supplier.objects.count(), 3)
        self.assertEqual(Item.objects.count(), 3)

    def test_get_items(self):
        response = self.client.get("/api/inventory/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_one_item(self):
        response = self.client.get(f"/api/inventory/items/{self.item1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Sony HeadPhones")

    def test_delete_item(self):
        response = self.client.delete(f"/api/inventory/items/{self.item1.id}")
        print(response)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(self.supplier1.items.count(), 1)
        self.assertEqual(self.supplier2.items.count(), 1)

    def test_get_supplier_items(self):
        response = self.client.get(
            f"/api/inventory/suppliers/{self.supplier1.id}/items/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Sony HeadPhones")
        self.assertEqual(response.data[1]["name"], "Nike Sneakers")

    def test_get_item_suppliers(self):
        response = self.client.get(f"/api/inventory/items/{self.item2.id}/suppliers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Tango User")
        self.assertEqual(response.data[1]["name"], "Fisher Admin")
