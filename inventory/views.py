from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Item, Supplier
from .serializers import ItemDetailSerializer, ItemSerializer, SupplierSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class SupplierViewSet(ModelViewSet):
    """
    ViewSet for handling Supplier CRUD operations.

    This ViewSet provides endpoints for listing, creating, updating, and deleting suppliers.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def list(self, request, *args, **kwargs):
        """
        List all suppliers.

        If no suppliers exist, it returns a 204 No Content response.
        """

        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            return Response(
                {"message": "No Items available."}, status=status.HTTP_204_NO_CONTENT
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a supplier instance.

        It returns a 204 No Content response upon successful deletion.
        """

        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Supplier deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ItemViewSet(ModelViewSet):
    """
    ViewSet for handling Item CRUD operations.

    This ViewSet provides endpoints for listing, creating, updating, retrieving, and deleting items.
    It also handles the association of suppliers with items during creation and update.
    """

    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action being performed.

        For create, retrieve, update, and partial_update actions, it returns the ItemDetailSerializer.
        For other actions, it returns the default ItemSerializer.
        """

        if self.action in ["create", "retrieve", "update", "partial_update"]:
            return ItemDetailSerializer
        return ItemSerializer

    def list(self, request, *args, **kwargs):
        """
        List all items.

        If no items exist, it returns a 204 No Content response.
        """

        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No Items available."}, status=status.HTTP_204_NO_CONTENT
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new item instance and associate it with the provided suppliers.

        It expects a list of supplier IDs in the 'suppliers' field of the request data.
        Upon successful creation, it returns the item data with a 201 Created status.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        supplier_ids = serializer.validated_data.get("suppliers", None)
        if supplier_ids is not None:
            serializer.validated_data.pop("suppliers")

        item = serializer.save()

        if supplier_ids is not None:
            for supplier_id in supplier_ids:
                item.suppliers.add(supplier_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing item instance and associate it with the provided suppliers.

        It expects a list of supplier IDs in the 'suppliers' field of the request data.
        Upon successful update, it returns the updated item data with a 200 OK status.
        """

        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        supplier_ids = serializer.validated_data.get("suppliers", None)
        if supplier_ids is not None:
            serializer.validated_data.pop("suppliers")

        item = serializer.save()

        if supplier_ids is not None:
            for supplier_id in supplier_ids:
                item.suppliers.add(supplier_id)

        return Response(
            {"message": "Updated Items successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an item instance.

        It returns a 204 No Content response upon successful deletion.
        """

        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
