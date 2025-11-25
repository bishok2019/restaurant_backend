# from rest_framework import filters
from django_filters import rest_framework as filters

from base.views import CustomGenericListView, CustomGenericRetrieveView

from .models import APILog
from .serializers import ApiLogsListSerializer, ApiLogsRetrieveSerializer


class APILogsFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name="created_at", lookup_expr="date")

    class Meta:
        model = APILog
        fields = [
            "method",
            "user_id",
            "status_code",
            "created_at",
            "created_at_bs",
        ]


class APILogsListView(CustomGenericListView):
    serializer_class = ApiLogsListSerializer
    queryset = APILog.objects.all()
    # filterset_fields = ["created_at", "created_at_bs"]
    filterset_class = APILogsFilter
    search_fields = [
        "url",
        "status_code",
    ]
    # def get_permissions(self):
    #     return [
    #         CustomAuthenticationPermission(
    #             models={
    #                 PermissionLists.HTTP_GET_METHOD: PermissionLists.API_LOGS,
    #             },
    #         )
    #     ]


class APILogsRetrieveView(CustomGenericRetrieveView):
    serializer_class = ApiLogsRetrieveSerializer
    queryset = APILog.objects.all()

    # def get_permissions(self):
    #     return [
    #         CustomAuthenticationPermission(
    #             models={
    #                 PermissionLists.HTTP_GET_METHOD: PermissionLists.API_LOGS,
    #             },
    #         )
    #     ]
