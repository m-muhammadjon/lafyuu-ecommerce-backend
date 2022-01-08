import django_filters

from shop.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='startswith')
    price_gte = django_filters.CharFilter(field_name='price', lookup_expr='gte', label='Price gte')
    price_lte = django_filters.CharFilter(field_name='price', lookup_expr='lte', label='Price lte')

    class Meta:
        model = Product
        fields = ['category', 'name']
