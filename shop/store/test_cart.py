# import json
# from models import Product, ShoppingCart, ShoppingCartItem
# from serializers import ProductSerializer

# product = Product.objects.all().first()
# cart = ShoppingCart()
# cart.save()
# item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=5)
# item.save()
# serializer = ProductSerializer(product)
# print(json.dumps(serializer.data, indent=2))

from datetime import datetime

# Define the start and end dates
start_date = datetime(2023, 9, 9)
end_date = datetime(2023, 9, 30)

# Get today's date
today = datetime.today()

# Check if today falls between the start and end dates
if start_date <= today <= end_date:
    print("Today falls between the start and end dates.")
else:
    print("Today does not fall between the start and end dates.")
