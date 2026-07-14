from jennie.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'

    
class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


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



class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = Cart
        fields = [
            "id",
            "items"
        ]