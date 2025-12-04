from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import Kitchen, Kitchen_Category


class Kitchen_CategoryListSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        exclude = ExcludeFields.exclude


class Kitchen_CategoryCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        exclude = ExcludeFields.exclude


class Kitchen_CategoryRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        exclude = ExcludeFields.exclude


class Kitchen_CategoryUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen_Category
        exclude = ExcludeFields.exclude


class KitchenListSerializer(BaseModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Kitchen
        exclude = ExcludeFields.exclude


class KitchenCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        exclude = ExcludeFields.exclude


class KitchenRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        exclude = ExcludeFields.exclude


class KitchenUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Kitchen
        exclude = ExcludeFields.exclude
