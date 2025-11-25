from django_filters import FilterSet, filters

from apps.location import models


class DistrictFilters(FilterSet):
    province_name = filters.CharFilter(
        field_name="province__name", lookup_expr="iexact", label="Province Name"
    )
    province_id = filters.NumberFilter(
        field_name="province__province_id", label="Nepal Province Id"
    )
    province_pk = filters.NumberFilter(field_name="province__id", label="Province Pk")

    class Meta:
        model = models.District
        fields = ["id", "name", "is_active"]
