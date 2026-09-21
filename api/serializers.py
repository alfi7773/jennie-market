from jennie.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('created_at', 'updated_at')


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        exclude = ('created_at', 'updated_at')

    
class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        exclude = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["id","full_name","phone","message","created_at"]



class CartItemSerializer(serializers.ModelSerializer):

    product = serializers.StringRelatedField()
    price = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "price"
        ]


    def get_price(self, obj):
        return obj.total_price()



class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    product_name = serializers.CharField(
        source="product.title",
        read_only=True
    )

    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",        
            "product_name",   
            "quantity",
            "price",
        ]

    def get_price(self, obj):
        return obj.total_price()