from rest_framework.generics import ListAPIView
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
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ("id",)
    search_fields = ("name", "description")
    pagination_class = ProductsPagination

    # filter a product by whether its on sale or not
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
