from rest_framework.test import APITestCase
from store.models import Product


class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            "name": "New Product",
            "description": "Some description.",
            "price": "120.50",
        }
        response = self.client.post("/api/v1/products/new", product_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(Product.objects.count(), initial_product_count + 1)
