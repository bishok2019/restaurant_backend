from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import OrderItem, Orders


class OrderListSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Orders
        exclude = ExcludeFields.exclude


class OrderItemListSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemCreateSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude


class OrderItemUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ExcludeFields.exclude
