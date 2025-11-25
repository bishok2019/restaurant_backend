from django_filters import rest_framework as filters

from apps.authentication.models.perms import Roles
from apps.authentication.models.user_profile import ContactUs

from ..models import CustomUser


class UserFilters(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(
        field_name="created_at",
        label="Created Between (start and end date)",
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "gender",
            "user_type",
            # "palika",
            # "municipallity",
            "district",
            "date_range",
            "is_active",
        ]


class ContactUsFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(
        field_name="created_at",
        label="Created Between (start and end date)",
    )

    class Meta:
        model = ContactUs
        fields = [
            "date_range",
        ]


class RolesFilter(filters.FilterSet):
    date_range = filters.DateFromToRangeFilter(
        field_name="created_at",
        label="Created Between (start and end date)",
    )

    class Meta:
        model = Roles
        fields = ["date_range", "is_active"]
