from django_filters import FilterSet, filters

from apps.location import models


class LocationFilters(FilterSet):
    district_name = filters.CharFilter(
        field_name="district__name", lookup_expr="iexact"
    )
    district_id = filters.NumberFilter(field_name="district__district_id")
    district_pk = filters.NumberFilter(field_name="district__id")

    province_name = filters.CharFilter(
        field_name="district__province__name", lookup_expr="iexact"
    )
    province_id = filters.NumberFilter(field_name="district__province__province_id")
    province_pk = filters.NumberFilter(field_name="district__province__id")

    class Meta:
        model = models.Palika
        fields = ["id", "name", "is_active"]
