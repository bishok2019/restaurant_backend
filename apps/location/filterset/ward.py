from django_filters import FilterSet, filters

from apps.location import models


class WardFilters(FilterSet):
    district_name = filters.CharFilter(
        field_name="location__district__name", lookup_expr="iexact"
    )
    district_id = filters.NumberFilter(field_name="location__district__district_id")
    district_pk = filters.NumberFilter(field_name="location__district__id")

    province_name = filters.CharFilter(
        field_name="location__district__province__name", lookup_expr="iexact"
    )
    province_id = filters.NumberFilter(
        field_name="location__district__province__province_id"
    )
    province_pk = filters.NumberFilter(field_name="location__district__province__id")

    location_name = filters.CharFilter(
        field_name="location__name", lookup_expr="iexact"
    )
    location_pk = filters.NumberFilter(field_name="location__id")
    location_id = filters.NumberFilter(field_name="location__location_id")

    class Meta:
        model = models.Ward
        fields = ["id", "number", "is_active"]
