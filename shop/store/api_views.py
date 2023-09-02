from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination


# import django_filters.rest_framework

from store.serializers import ProductSerializer
from store.models import Product


class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # filter back ends with URL Query
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # http://127.0.0.1:8000/api/v1/products/
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ("id",)
    # http://127.0.0.1:8000/api/v1/products/?id=2
    search_fields = ("name", "description")
    # http://127.0.0.1:8000/api/v1/products/?search=knife
    pagination_class = ProductsPagination
    # http://127.0.0.1:8000/api/v1/products/?limit=2

    # filter a product by whether its on sale or not
    # http://127.0.0.1:8000/api/v1/products/?on_sale=true
    def get_queryset(self):
        on_sale = self.request.query_params.get("on_sale", None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == "true":
            from django.utils import timezone

            now = timezone.now()
            return queryset.filter(sale_start__lte=now, sale_end__gte=now)
        return queryset


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get("price")
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"price": "Must be above $0.00"})
        except ValueError:
            raise ValidationError({"price": "A valid number is required"})
        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroy):
    queryset = Product.objects.all()
    lookup_field = "id"
    serializer_class = ProductSerializer


# delete cached cookies for the deleted item


def delete(self, request, *args, **kwargs):
    product_id = request.data.get("id")
    response = super().delete(request, *args, **kwargs)
    if response.status_code == 204:
        from django.core.cache import cache

        cache.delete("product_data_{}".format(product_id))
    return response


# example url to destroy item with id #2 -> http://127.0.0.1:8000/api/v1/products/2/destroy
