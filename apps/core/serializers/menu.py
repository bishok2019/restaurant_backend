from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import Menu, MenuItem


class MenuListSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        fields = ExcludeFields.exclude


class MenuCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        fields = ExcludeFields.exclude


class MenuRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        fields = ExcludeFields.exclude


class MenuUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Menu
        fields = ExcludeFields.exclude


class MenuItemMenuListSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        fields = ExcludeFields.exclude


class MenuItemMenuCreateSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        fields = ExcludeFields.exclude


class MenuItemRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        fields = ExcludeFields.exclude


class MenuItemUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = MenuItem
        fields = ExcludeFields.exclude
