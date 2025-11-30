from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Menu
from ..serializers import (
    EmployeeListSerializer,
    EmployeeRetrieveSerializer,
    EmployeeUpdateSerializer,
    MenuCreateSerializer,
)


class MenuListApiView(CustomGenericListView):
    serializer_class = EmployeeListSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Fetched Successfully"


class MenuCreateApiView(CustomGenericCreateView):
    serializer_class = MenuCreateSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Fetched Successfully"


class MenuRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = EmployeeRetrieveSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Fetched Successfully"


class MenuUpdateApiView(CustomGenericUpdateView):
    serializer_class = EmployeeUpdateSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Fetched Successfully"
