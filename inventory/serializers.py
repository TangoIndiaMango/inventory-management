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

    def update(self, instance, validated_data):
        # Update Supplier fields
        instance.name = validated_data.get("name", instance.name)
        instance.contact_info = validated_data.get("contact_info", instance.contact_info)
        instance.save()

        # Update Items relationship
        items_data = validated_data.pop("items", [])
        existing_items = {item.id: item for item in Item.objects.all()}
        existing_item_ids = set(existing_items.keys())

        items_to_create = []
        items_to_update = []
        items_to_add = []

        for item_data in items_data:
            if isinstance(item_data, dict):
                item_id = item_data.get("id")
                if item_id in existing_item_ids:
                    items_to_update.append(item_data)
                else:
                    items_to_create.append(item_data)
            elif isinstance(item_data, int) and item_data in existing_item_ids:
                items_to_add.append(item_data)
            else:
                raise serializers.ValidationError(f"Invalid item data. {item_data}")

        # Create new items
        created_items = Item.objects.bulk_create([Item(**data) for data in items_to_create])

        # Update existing items
        for data in items_to_update:
            Item.objects.filter(id=data["id"]).update(**data)

        # Add created and updated items to the supplier
        for item in created_items:
            instance.items.add(item)
        for item_id in items_to_add:
            instance.items.add(existing_items[item_id])

        return instance

class SupplierDataWithoutItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "contact_info", "created_at", "updated_at"]
