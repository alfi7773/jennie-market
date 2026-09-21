import django_filters
from jennie.models import Product

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains", label="Поиск по названию")
    
    color = django_filters.NumberFilter(field_name="colors__id", label="ID цвета")

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'material': ['exact'],
            'price': ['exact', 'gte', 'lte'],  
            'country': ['exact', 'icontains'],
        }
