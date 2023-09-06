from rest_framework import serializers
from store.models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = ShoppingCartItem
        fields = ("product", "quantity")


# simplified custom fields by replacing the fields in the representation method
# and refactor them using serializer fields


class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)
    cart_items = serializers.SerializerMethodField()
    # price = serializers.FloatField(min_value=1.00, max_value=10000.00)
    price = serializers.DecimalField(
        min_value=1.00,
        max_value=100000,
        max_digits=None,
        decimal_places=2,
    )
    sale_start = serializers.DateTimeField(
        input_formats=["%m-%d-%Y"],
        format=None,
        allow_null=True,
        help_text='Accepted format is "12-25-2023"',
        style={"input_type": "text"},
    )
    sale_end = serializers.DateTimeField(
        input_formats=["%m-%d-%Y"],
        format=None,
        allow_null=True,
        help_text='Accepted format is "12-25-2023"',
        style={"input_type": "text"},
    )
    photo = serializers.ImageField(default=None)
    # write_only=True means that the serailzier can write to the
    # field but it does not get saved to the model
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "sale_start",
            "sale_end",
            "is_on_sale",
            "current_price",
            "cart_items",
            "photo",
            "warranty",
        )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    #  Validated data in the update method is the data that will be used to update the model. It is safe to access
    #  because it is already passed through the validation process.
    def update(self, instance, validated_data):
        if validated_data.get("warranty", None):
            instance.description += "\n\nWarranty Information:\n"
            instance.description += b"; ".join(
                validated_data["warranty"].readlines()
            ).decode()
        return instance


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField())
    )
