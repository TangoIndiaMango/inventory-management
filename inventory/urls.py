from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, SupplierViewSet

router = DefaultRouter(trailing_slash=False)

router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
]
