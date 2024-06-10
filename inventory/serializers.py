from rest_framework import serializers

from .models import Item, Supplier


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True, read_only=True)
    items = serializers.SerializerMethodField("get_items")

    class Meta:
        model = Supplier
        fields = "__all__"

    def get_items(self, obj):
        return {item.id: item.name for item in obj.items.all()}

class SupplierDetailSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, required=False)
    items_data = serializers.SerializerMethodField("get_items")

    class Meta:
        model = Supplier
        fields = "__all__"

    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def get_items(self, obj):
        return [f"{item.id}: {item.name}" for item in obj.items.all()]

    def to_internal_value(self, data):
        items_data = data.pop("items", [])
        data = super().to_internal_value(data)
        data["items"] = items_data
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        items_data = data.pop("items", [])
        data["items"] = items_data
        return data



class SupplierDataWithoutItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "contact_info", "created_at", "updated_at"]
