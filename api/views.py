from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import *
from .serializers import *


@extend_schema(
    tags=["категории"],
    summary="получить список товаров по фильтрам",
    description="возвращает список товаров с фильтрацией.",
    parameters=[
        OpenApiParameter(
            name="category",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID категории"
        ),
        OpenApiParameter(
            name="color",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID цвета"
        ),
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="поиск по названию товара"
        ),
    ],
)
class CategoryAPIView(APIView):

    def get(self, request):
        queryset = Product.objects.all()

        category = request.query_params.get("category")
        color = request.query_params.get("color")
        search = request.query_params.get("search")

        if category:
            queryset = queryset.filter(category_id=category)

        if color:
            queryset = queryset.filter(colors__id=color)

        if search:
            queryset = queryset.filter(title__icontains=search)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["цвета"],
    summary="получить список цветов",
    description="возвращает список цветов с возможностью поиска.",
    parameters=[
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="поиск по названию цвета"
        ),
    ],
)
class ColorAPIView(APIView):

    def get(self, request):
        colors = Color.objects.all()

        search = request.query_params.get("search")

        if search:
            colors = colors.filter(title__icontains=search)

        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["материалы"],
    summary="получить список материалов",
    description="возвращает список материалов с возможностью поиска.",
    parameters=[
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="поиск по названию материала"
        ),
    ],
)
class MaterialAPIView(APIView):

    def get(self, request):
        materials = Material.objects.all()

        search = request.query_params.get("search")

        if search:
            materials = materials.filter(title__icontains=search)

        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["товары"],
    summary="получить список товаров",
    description="возвращает список товаров с фильтрацией.",
    parameters=[
        OpenApiParameter(
            name="category",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID категории"
        ),
        OpenApiParameter(
            name="color",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID цвета"
        ),
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="поиск по названию товара"
        ),
    ],
)
class ProductAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()

        category = request.query_params.get("category")
        color = request.query_params.get("color")
        search = request.query_params.get("search")

        if category:
            products = products.filter(category_id=category)

        if color:
            products = products.filter(colors__id=color)

        if search:
            products = products.filter(title__icontains=search)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["контакты"],
    summary="отправить заявку"
)
class ContactCreateAPIView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@extend_schema(
    tags=["корзина"],
    summary="добавить товар в корзину"
)
class CartItemViewSet(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer