from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class CustomPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_query_param = "offset"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "message": "Data retrieved successfully.",
                "data": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )


class CustomFilterOrderingSearchMixin:
    """
    Mixin for adding filtering, searching, ordering, and pagination capabilities to API views.
    """

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    search_fields = []
    ordering_fields = []
    ordering = "-created_at"

    filter_fields = []

    # must define filter fields as a list of tuples (field_name, field_type)
    filter_logic = {
        "date": lambda field, value: {f"{field}__date": value},
        "boolean": lambda field, value: {field: value.lower() in ["true", "1"]},
        "text": lambda field, value: {field: value},
        "id": lambda field, value: {field: value},
    }

    def get_queryset(self):
        """
        Override this method to return the queryset you want to filter and sort.
        """
        raise NotImplementedError("You must define 'get_queryset' in subclasses.")

    def get_serializer_class(self):
        """
        You can override this method to return a different serializer class based on conditions.
        """
        raise NotImplementedError(
            "You must define 'get_serializer_class' in subclasses."
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_params = {}
        for field, field_type in self.filter_fields:
            param_value = request.query_params.get(field)
            """
            logic : get all query params and check if they are in the filter_fields[] 
            then proceed with each params validation and store it in filter_params dictionary 
            and at last use that to apply filter to the queryset
            """
            if param_value is not None and field_type in self.filter_logic:
                try:
                    if field_type == "date":
                        parsed_date = timezone.make_aware(
                            datetime.strptime(param_value, "%Y-%m-%d")
                        )
                        filter_params.update(
                            self.filter_logic[field_type](field, parsed_date)
                        )
                    elif field_type == "id":
                        try:
                            filter_params[field] = int(param_value)
                        except ValueError:
                            return self.custom_error_response(
                                message=f"Invalid ID format for {field}. Must be an integer.",
                                status_code=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        filter_params.update(
                            self.filter_logic[field_type](field, param_value)
                        )
                except ValueError:
                    return self.custom_error_response(
                        message=f"Invalid format for field: {field}.",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

        # apply filtering
        if filter_params:
            queryset = queryset.filter(**filter_params)

        # apply searching
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        # apply ordering
        ordering_params = request.query_params.get("order_by")

        if not ordering_params:
            ordering_params = self.ordering if self.ordering else None

        if ordering_params and ordering_params in self.ordering_fields:
            queryset = queryset.order_by(*ordering_params.split(","))

        # apply pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # serialize data
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class CustomAccessToken(AccessToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_user_info()

    def set_user_info(self):
        self["extra_data"] = "helloworld"


class CustomRefreshToken(RefreshToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_user_info()

    def set_user_info(self):
        self["extra_data"] = "helloworld"


class CustomAPIResponse:
    # this is custom api response for success and error used in both API VIew and generic viewsets

    @staticmethod
    def custom_success_response(
        data=None, message="Success", detail=None, status_code=status.HTTP_200_OK
    ):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": True,
            "message": message,
            "detail": detail,
            "data": data,
            "meta_data": meta_data,
        }
        return Response(response, status=status_code)

    @staticmethod
    def custom_error_response(
        message="An error occurred",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=None,
    ):
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        response = {
            "success": False,
            "message": message,
            "errors": errors or {},
            "detail": detail,
            "meta_data": meta_data,
        }
        return Response(response, status=status_code)


class BaseAPIView(CustomAPIResponse, APIView):
    serializer_class = None

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, ValidationError):
            return self.custom_error_response(
                message="Validation failed.", errors=response.data
            )
        return response


class BaseModelViewSet(CustomAPIResponse, viewsets.ModelViewSet):
    def handle_exception(self, exc):
        # get the exception respnse of DRF from exception handler
        response = super().handle_exception(exc)
        if isinstance(exc, ValidationError):
            return self.custom_error_response(
                message="Validation failed.", errors=response.data
            )
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.custom_success_response(
            data=serializer.data,
            message="Created successfully!",
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.custom_success_response(
            data=serializer.data, message="Updated successfully!"
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.custom_success_response(
            message="Deleted successfully!", status_code=status.HTTP_204_NO_CONTENT
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.custom_success_response(
            data=serializer.data, message="Retrieved successfully!"
        )

    def list(self, request, *args, **kwargs):
        self.request_action = "list"
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.custom_success_response(
            data=serializer.data, message="List retrieved successfully!"
        )


class ListGenericView(ListAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["id", "created_at"]
    ordering = "-created_at"
    request_action = "list"
