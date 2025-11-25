from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from apps.location import filterset, models, serializers
from base.views.generic_views import CustomGenericListView
from base.views.views import BaseAPIView, ListGenericView


class ProvinceListView(CustomGenericListView):
    """
    PK refers to the Primary Key which is we are using for our db.\n
    \t** Don't get confused with the province_id, district_id, location_id and with the db id. ** \n
    \t province_id refers to the province id that GOV of Nepal has declared,\n
    \t and respectively for the district_id, and location_id.\n
    We are sticking to that, for working with the id we'll be using pk for our ease.
    """

    queryset = models.Province.objects.filter(is_active=True)
    serializer_class = serializers.ProvinceSerializer
    filterset_class = filterset.ProvinceFilters

    search_fields = ["id", "name"]
    permission_classes = []


class DistrictListView(CustomGenericListView):
    """
    PK refers to the Primary Key which is we are using for our db.\n
    \t** Don't get confused with the province_id, district_id, location_id and with the db id. ** \n
    \t province_id refers to the province id that GOV of Nepal has declared.\n
    \t and respectively for the district_id, and location_id.\n
    We are sticking to that, for working with the id we'll be using pk for our ease.
    """

    queryset = models.District.objects.filter(is_active=True)
    serializer_class = serializers.DistrictSerializer
    filterset_class = filterset.DistrictFilters
    permission_classes = []

    search_fields = ["id", "name", "province__name"]


class PalikaListView(CustomGenericListView):
    """
    PK refers to the Primary Key which is we are using for our db.\n
    \t** Don't get confused with the province_id, district_id, location_id and with the db id. ** \n
    \t province_id refers to the province id that GOV of Nepal has declared.\n
    \t and respectively for the district_id, and location_id.\n
    We are sticking to that, for working with the id we'll be using pk for our ease.
    """

    queryset = models.Palika.objects.filter(is_active=True)
    serializer_class = serializers.PalikaSerializer
    filterset_class = filterset.LocationFilters

    permission_classes = []
    search_fields = ["id", "name", "district__name", "district__province__name"]


class WardListView(CustomGenericListView):
    """
    PK refers to the Primary Key which is we are using for our db.\n
    \t** Don't get confused with the province_id, district_id, location_id and with the db id. ** \n
    \t province_id refers to the province id that GOV of Nepal has declared.\n
    \t and respectively for the district_id, and location_id.\n
    We are sticking to that, for working with the id we'll be using pk for our ease.
    """

    queryset = models.Ward.objects.filter(is_active=True)
    serializer_class = serializers.WardSerializer
    filterset_class = filterset.WardFilters

    permission_classes = []
    search_fields = [
        "id",
        "name",
        "location__name",
        "location__district__name",
        "location__district__province__name",
    ]
