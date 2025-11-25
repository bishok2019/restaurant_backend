from apps.location import models
from base.serializers import BaseModelSerializer, ExcludeFields, serializers


class ProvinceSerializer(BaseModelSerializer):
    province_pk = serializers.IntegerField(source="pk", read_only=True)

    class Meta:
        model = models.Province
        exclude = ExcludeFields.exclude


class DistrictSerializer(BaseModelSerializer):
    district_pk = serializers.IntegerField(source="pk", read_only=True)
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = models.District
        exclude = ExcludeFields.exclude


class PalikaSerializer(BaseModelSerializer):
    location_pk = serializers.IntegerField(source="pk", read_only=True)
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = models.Palika
        exclude = ExcludeFields.exclude


class WardSerializer(BaseModelSerializer):
    location = PalikaSerializer(read_only=True)

    class Meta:
        model = models.Ward
        exclude = ExcludeFields.exclude
