from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GetItemsSupplier, GetSupplierItems, ItemViewSet, RemoveItemFromSupplier, SupplierViewSet

router = DefaultRouter(trailing_slash=False)

router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("items", ItemViewSet, basename="items")

urlpatterns = [
    path("", include(router.urls)),
    path('suppliers/<int:supplier_id>/items/', GetSupplierItems.as_view(), name='supplier-items'),
    path('items/<int:item_id>/suppliers/', GetItemsSupplier.as_view(), name='item-suppliers'),
    path('suppliers/<int:supplier_id>/remove/<int:item_id>', RemoveItemFromSupplier.as_view(), name='remove-item-from-supplier')
]
