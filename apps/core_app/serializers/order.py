from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import OrderItem, Orders


class OrderListSerializer(BaseModelSerializer):
    model = Orders
    exclude = ExcludeFields.exclude


class OrderCreateSerializer(BaseModelSerializer):
    model = Orders
    exclude = ExcludeFields.exclude


class OrderRetrieveSerializer(BaseModelSerializer):
    model = Orders
    exclude = ExcludeFields.exclude


class OrderUpdateSerializer(BaseModelSerializer):
    model = Orders


class OrderItemListSerializer(BaseModelSerializer):
    model = OrderItem
    exclude = ExcludeFields.exclude


class OrderItemCreateSerializer(BaseModelSerializer):
    model = OrderItem
    exclude = ExcludeFields.exclude


class OrderItemRetrieveSerializer(BaseModelSerializer):
    model = OrderItem
    exclude = ExcludeFields.exclude


class OrderItemUpdateSerializer(BaseModelSerializer):
    model = OrderItem
    exclude = ExcludeFields.exclude
