from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Категории"],
    summary="Получить список категорий",
    description="Возвращает список всех категорий с возможностью поиска и сортировки",
    parameters=[
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поиск по названию категории",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поле для сортировки результатов. Например: title, -title, order, -order",
            enum=["title", "-title", "order", "-order", "created_at", "-created_at"],
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
    },
)
class CategoryAPIView(APIView):
    def get(self, request):
        queryset = Category.objects.all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["Цвета"],
    summary="Получить список цветов",
    description="Возвращает список всех цветов с возможностью поиска",
    parameters=[
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поиск по названию цвета",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поле для сортировки результатов",
            enum=["title", "-title", "created_at", "-created_at"],
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
    },
)
class ColorAPIView(APIView):
    def get(self, request):
        queryset = Color.objects.all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = ColorSerializer(queryset, many=True)
        return Response(serializer.data)




@extend_schema(
    tags=["Материалы"],
    summary="Получить список материалов",
    description="Возвращает список всех материалов с возможностью поиска",
    parameters=[
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поиск по названию материала",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поле для сортировки результатов",
            enum=["title", "-title", "created_at", "-created_at"],
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
    },
)
class MaterialAPIView(APIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request):
        queryset = self.queryset.all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        ordering = request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

@extend_schema(
    tags=["Товары"],
    summary="Получить список товаров",
    description="Возвращает список товаров с фильтрацией по категории, цвету, материалу и поиском. Пагинация: 12 товаров на страницу.",
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID категории для фильтрации",
        ),
        OpenApiParameter(
            name="material",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID материала для фильтрации",
        ),
        OpenApiParameter(
            name="color",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="ID цвета для фильтрации",
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поиск по названию товара",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Поле для сортировки результатов",
        ),
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Номер страницы для пагинации",
        ),
    ],
)
class ProductAPIView(APIView):

    def get(self, request, pk=None):

        # Если передан ID — возвращаем один товар
        if pk is not None:
            product = get_object_or_404(Product, id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        # Если ID не передан — возвращаем список товаров
        queryset = Product.objects.all()

        category = request.query_params.get("category")
        color = request.query_params.get("color")
        material = request.query_params.get("material")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")

        if category:
            queryset = queryset.filter(category_id=category)

        if color:
            queryset = queryset.filter(colors__id=color)

        if material:
            queryset = queryset.filter(material_id=material)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if ordering:
            queryset = queryset.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 12

        paginated_queryset = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = ProductSerializer(
            paginated_queryset,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

@extend_schema(
    tags=["Контакты"],
    summary="Отправить заявку",
    description="Отправляет заявку на обратную связь",
    request=ContactSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
)
class ContactCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()



            return Response(
                {"message": "Заявка успешно отправлена"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=["Корзина"],
    summary="Добавить товар в корзину",
    request=CartItemSerializer,
    responses={201: CartItemSerializer},
)
class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create()

        serializer.save(cart=cart)