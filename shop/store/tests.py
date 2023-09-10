from rest_framework.test import APITestCase

from store.models import Product


class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            "name": "New Product",
            "description": "Awesome product",
            "price": "123.45",
        }
        response = self.client.post("/api/v1/products/new", product_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data["is_on_sale"], False)
        self.assertEqual(
            response.data["current_price"],
            float(product_attrs["price"]),
        )


class ProductDestroyTestCase(APITestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name="Test Product", description="Test Description", price=10.99
        )

    def test_delete_product(self):
        initial_product_count = Product.objects.count()
        product_id = self.product.id  # use the ID of the test product
        self.client.delete("/api/v1/products/{}/".format(product_id))
        self.assertEqual(
            Product.objects.count(),
            initial_product_count - 1,
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get,
            id=product_id,
        )


class ProductListTestCase(APITestCase):
    def test_list_products(self):
        products_count = Product.objects.count()
        response = self.client.get("/api/v1/products/")
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(response.data["count"], products_count)
        self.assertEqual(len(response.data["results"]), products_count)
