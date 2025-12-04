from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import OrderItem, Orders


class OrderListSerializer(BaseModelSerializer):
    served_by = serializers.CharField(source="served_by.user.username", read_only=True)

    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderRetrieveSerializer(BaseModelSerializer):
    served_by = serializers.CharField(source="served_by.user.username", read_only=True)

    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderItemListSerializer(BaseModelSerializer):
    order_item = serializers.CharField(source="order_item.name")
    order = serializers.CharField(source="order.table_number")

    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemCreateSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemRetrieveSerializer(BaseModelSerializer):
    order_item = serializers.CharField(source="order_items.name")
    order = serializers.CharField(source="order.table_number")

    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude
