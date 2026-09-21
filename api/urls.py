from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as url_doc

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
\


router = DefaultRouter()
# router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('materials/', MaterialAPIView.as_view()),
    path('colors/', ColorAPIView.as_view()),
    path("products/", ProductAPIView.as_view()),
    path("products/<int:pk>/", ProductAPIView.as_view()),
    path('contact/',ContactCreateAPIView.as_view()),
    path('cart/', CartItemCreateView.as_view()),
    path('', include(router.urls)),
]

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)