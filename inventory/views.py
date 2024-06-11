from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Item, Supplier
from .serializers import (
    ItemSerializer,
    SupplierDataWithoutItemsSerializer,
    SupplierDetailSerializer,
    SupplierSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.


class ItemViewSet(ModelViewSet):
    """
    ViewSet for handling Item CRUD operations.

    This ViewSet provides endpoints for listing, creating, updating, and deleting Items.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request, *args, **kwargs):
        """
        List all Items.

        If no Item exist, it returns a 204 No Content response.
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
        Delete an Item instance.

        It returns a 204 No Content response upon successful deletion.
        """

        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SupplierViewSet(ModelViewSet):
    """
    ViewSet for handling Supplier CRUD operations.

    This ViewSet provides endpoints for listing, creating, updating, retrieving, and deleting Suppliers.
    It also handles the association of suppliers with Suppliers during creation and update.
    """

    queryset = Supplier.objects.all().order_by("-created_at")
    serializer_class = SupplierSerializer

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action being performed.

        For create, retrieve, update, and partial_update actions, it returns the SupplierDetailSerializer.
        For other actions, it returns the default SupplierSerializer.
        """

        if self.action in ["create", "update", "partial_update"]:
            return SupplierDetailSerializer
        return SupplierSerializer

    def list(self, request, *args, **kwargs):
        """
        List all suppliers.

        If no supplier exist, it returns a 204 No Content response.
        """

        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"message": "No Suppliers available."},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new item instance and associate it with the provided items.

        It expects a list of items IDs in the 'items' field of the request data.
        Upon successful creation, it returns the item data with a 201 Created status.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data.get("items", [])

        if items_data is None:
            return Response(
                {"message": "At least one item is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.validated_data.pop("items")

        supplier = serializer.save()
        
        existing_item_ids = []
        new_items = []
        
        for item in items_data:
            if isinstance(item, dict):
                new_items.append(Item(**item))
            else:
                existing_item_ids.append(int(item))
            
        created_items = Item.objects.bulk_create(new_items)
        supplier.items.add(*created_items)
        
        existing_items = Item.objects.filter(id__in=existing_item_ids)
        supplier.items.add(*existing_items)
        
        serializer = self.get_serializer(supplier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing item instance and associate it with the provided items.

        It expects a list of item IDs in the 'items' field of the request data.
        Upon successful update, it returns the updated item data with a 200 OK status.
        """

        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Updated Supplier successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )

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


class GetSupplierItems(APIView):
    """
    View for handling all the Items supplied by a supplier.
    """

    def get(self, request, supplier_id, *args, **kwargs):
        """
        Retrieve all the Items supplied by a supplier.

        It returns a list of Item data with a 200 OK status.
        """

        supplier = get_object_or_404(Supplier, id=supplier_id)

        items = supplier.items.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetItemsSupplier(APIView):
    """
    View for handling all the Items supplied by a supplier.
    """

    def get(self, request, item_id, *args, **kwargs):
        """
        Retrieve all the Suppliers for an item.

        It returns a list of suppliers data with a 200 OK status.
        """

        items = get_object_or_404(Item, id=item_id)

        suppliers = items.suppliers.all()
        serializer = SupplierDataWithoutItemsSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
