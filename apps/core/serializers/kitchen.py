from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import Kitchen, Kitchen_Category


class Kitchen_CategoryListSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        fields = ExcludeFields.exclude


class Kitchen_CategoryCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        fields = ExcludeFields.exclude


class Kitchen_CategoryRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        fields = ExcludeFields.exclude


class Kitchen_CategoryUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        fields = ExcludeFields.exclude


class KitchenListSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        fields = ExcludeFields.exclude


class KitchenCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        fields = ExcludeFields.exclude


class KitchenRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        fields = ExcludeFields.exclude


class KitchenUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        fields = ExcludeFields.exclude
