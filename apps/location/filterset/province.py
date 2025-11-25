from django_filters import FilterSet

from apps.location import models


class ProvinceFilters(FilterSet):
    class Meta:
        model = models.Province
        fields = ["id", "name", "is_active"]
