from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Employee
from ..serializers import (
    EmployeeCreateSerializer,
    EmployeeListSerializer,
    EmployeeRetrieveSerializer,
    EmployeeUpdateSerializer,
)


class EmployeeListApiView(CustomGenericListView):
    serializer_class = EmployeeListSerializer
    queryset = Employee.objects.all()
    success_response_message = "Employee Fetched Successfully"


class EmployeeCreateApiView(CustomGenericCreateView):
    serializer_class = EmployeeCreateSerializer
    queryset = Employee.objects.all()
    success_response_message = "Employee Created Successfully"


class EmployeeRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = EmployeeRetrieveSerializer
    queryset = Employee.objects.all()
    success_response_message = "Employee Retrieved Successfully"


class EmployeeUpdateApiView(CustomGenericUpdateView):
    serializer_class = EmployeeUpdateSerializer
    queryset = Employee.objects.all()
    success_response_message = "Employee Fetched Successfully"
