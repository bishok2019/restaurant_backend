from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import Menu, MenuItem


class MenuListSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        exclude = ExcludeFields.exclude


class MenuCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        exclude = ExcludeFields.exclude


class MenuRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        exclude = ExcludeFields.exclude


class MenuUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        exclude = ExcludeFields.exclude


class MenuItemListSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    kitchen = serializers.CharField(source="kitchen.name", read_only=True)

    class Meta:
        model = MenuItem
        exclude = ExcludeFields.exclude


class MenuItemCreateSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ExcludeFields.exclude


class MenuItemRetrieveSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name")
    kitchen = serializers.CharField(source="kitchen.name")

    class Meta:
        model = MenuItem
        exclude = ExcludeFields.exclude


class MenuItemUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        exclude = ExcludeFields.exclude
