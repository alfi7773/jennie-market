from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Material)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'price',
                    'country',
                    'category',
                    'material',
                    'is_new',
                    'is_sale',
                    'is_trend',
                    )

# Register your models here.
