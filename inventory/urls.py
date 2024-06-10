from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GetItemsSupplier, GetSupplierItems, ItemViewSet, SupplierViewSet

router = DefaultRouter(trailing_slash=False)

router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
    path('suppliers/<int:supplier_id>/items/', GetSupplierItems.as_view(), name='supplier-items'),
    path('items/<int:item_id>/suppliers/', GetItemsSupplier.as_view(), name='item-suppliers'),
]
