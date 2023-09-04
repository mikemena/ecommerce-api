import json
from models import Product, ShoppingCart, ShoppingCartItem
from serializers import ProductSerializer

product = Product.objects.all().first()
cart = ShoppingCart()
cart.save()
item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=5)
item.save()
serializer = ProductSerializer(product)
print(json.dumps(serializer.data, indent=2))
