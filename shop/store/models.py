# from django.utils import timezone
from datetime import datetime, date
from django.db import models
from decimal import Decimal


class Product(models.Model):
    DISCOUNT_RATE = 0.10
    print("discount rate type:", type(DISCOUNT_RATE))

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_start = models.DateField(blank=True, null=True, default=None)
    sale_end = models.DateField(blank=True, null=True, default=None)
    photo = models.ImageField(blank=True, null=True, default=None, upload_to="products")

    def is_on_sale(self):
        # dt = datetime(2023, 9, 9, 14, 30, 45)
        # d = dt.date()
        today = date.today()
        # print("type of dt: ", type(dt))
        # print("type of d: ", type(d))
        print("type of today: ", type(today))
        print("self.sale_start: ", self.sale_start)
        if self.sale_start:
            if self.sale_end:
                return self.sale_start <= today <= self.sale_end
            return self.sale_start <= today
        return False

    def get_rounded_price(self):
        return round(self.price, 2)

    def current_price(self):
        if self.is_on_sale():
            discounted_price = Decimal(self.price) * (1 - Decimal(self.DISCOUNT_RATE))
            return round(discounted_price, 2)
        return self.get_rounded_price()

    def __repr__(self):
        return '<Product object ({}) "{}">'.format(self.id, self.name)


class ShoppingCart(models.Model):
    TAX_RATE = 0.13

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def subtotal(self):
        amount = 0.0
        for item in self.shopping_cart_items:
            amount += item.quantity * item.product.get_price()
        return round(amount, 2)

    def taxes(self):
        return round(self.TAX_RATE * self.subtotal(), 2)

    def total(self):
        return round(self.subtotal() * self.taxes(), 2)

    def __repr__(self):
        name = self.name or "[Guest]"
        address = self.address or "[No Address]"
        return '<ShoppingCart object ({}) "{}" "{}">'.format(self.id, name, address)


class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        related_name="items",
        related_query_name="item",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, related_name="+", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total(self):
        return round(self.quantity * self.product.current_price())

    def __repr__(self):
        return '<ShoppingCartItem object ({}) {}x "{}">'.format(
            self.id, self.quantity, self.product.name
        )
