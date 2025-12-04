from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Menu, MenuItem
from ..serializers import (
    MenuCreateSerializer,
    MenuItemCreateSerializer,
    MenuItemListSerializer,
    MenuItemRetrieveSerializer,
    MenuItemUpdateSerializer,
    MenuListSerializer,
    MenuRetrieveSerializer,
    MenuUpdateSerializer,
)


class MenuListApiView(CustomGenericListView):
    serializer_class = MenuListSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Fetched Successfully"


class MenuCreateApiView(CustomGenericCreateView):
    serializer_class = MenuCreateSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Created Successfully"


class MenuRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = MenuRetrieveSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Retrieved Successfully"


class MenuUpdateApiView(CustomGenericUpdateView):
    serializer_class = MenuUpdateSerializer
    queryset = Menu.objects.all()
    success_response_message = "Menu Updated Successfully"


class MenuItemListApiView(CustomGenericListView):
    serializer_class = MenuItemListSerializer
    queryset = MenuItem.objects.all()
    success_response_message = "Menu Items Fetched Successfully"


class MenuItemCreateApiView(CustomGenericCreateView):
    serializer_class = MenuItemCreateSerializer
    queryset = MenuItem.objects.all()
    success_response_message = "Menu Item Created Successfully"


class MenuItemRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = MenuItemRetrieveSerializer
    queryset = MenuItem.objects.all()
    success_response_message = "Menu Item Retrieved Successfully"


class MenuItemUpdateApiView(CustomGenericUpdateView):
    serializer_class = MenuItemUpdateSerializer
    queryset = MenuItem.objects.all()
    success_response_message = "Menu Item Updated Successfully"
