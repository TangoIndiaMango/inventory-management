from rest_framework import serializers

from .models import Item, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    # items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    items = serializers.SerializerMethodField("get_items")

    class Meta:
        model = Supplier
        fields = "__all__"

    def get_items(self, obj):
        return {item.id:item.name for item in obj.items.all()}

class ItemSerializer(serializers.ModelSerializer):
    # suppliers = SupplierSerializer(many=True, read_only=True)
    suppliers = serializers.SerializerMethodField("get_suppliers")


    class Meta:
        model = Item
        fields = "__all__"
        
    def get_suppliers(self, obj):
        return {item.id:item.name for item in obj.suppliers.all()}

class ItemDetailSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), many=True
    )
    supplier_data = serializers.SerializerMethodField("get_suppliers")

    class Meta:
        model = Item
        fields = '__all__'
    
    
    def to_internal_value(self, data):
        if "suppliers" in data and isinstance(data["suppliers"], int):
            data["suppliers"] = [data["suppliers"]]
        return super().to_internal_value(data)

    def validate_supplier_id(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one supplier is required.")
        if not isinstance(value, list):
            value = [value]
        return value
    
    def get_suppliers(self, obj):
        return [f"{supplier.id}: {supplier.name}" for supplier in obj.suppliers.all()]


class ItemDataWithoutSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'created_at']
        
class SupplierDataWithoutItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_info', 'created_at']