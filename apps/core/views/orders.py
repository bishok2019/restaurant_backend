from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import OrderItem, Orders
from ..serializers import (
    OrderCreateSerializer,
    OrderItemCreateSerializer,
    OrderItemListSerializer,
    OrderItemRetrieveSerializer,
    OrderItemUpdateSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    OrderUpdateSerializer,
)

# OrderItem


class OrdersItemCreateApiView(CustomGenericCreateView):
    serializer_class = OrderItemCreateSerializer
    settings = "Orders Item Created Successfully."
    success_response_message = OrderItem.objects.all()


class OrdersItemListApiView(CustomGenericListView):
    serializer_class = OrderItemListSerializer
    queryset = OrderItem.objects.all()
    success_response_message = "OrderCreated Successfully."


class OrdersItemRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = OrderItemRetrieveSerializer
    queryset = OrderItem.objects.all()
    success_response_message = "OrderCreated Successfully."


class OrdersItemUpdateApiView(CustomGenericUpdateView):
    serializer_class = OrderItemUpdateSerializer
    queryset = OrderItem.objects.all()
    success_response_message = "OrderCreated Successfully."


# Order


class OrdersCreateApiView(CustomGenericCreateView):
    serializer_class = OrderCreateSerializer
    queryset = Orders.objects.all()
    success_response_message = "Order Created Successfully."


class OrdersListApiView(CustomGenericListView):
    serializer_class = OrderListSerializer
    queryset = Orders.objects.all()
    success_response_message = "Orders Fetched Successfully."


class OrdersRetrieveApiView(CustomGenericListView):
    serializer_class = OrderRetrieveSerializer
    queryset = Orders.objects.all()
    success_response_message = "Order Retrieved Successfully."


class OrdersUpdateApiView(CustomGenericUpdateView):
    serializer_class = OrderUpdateSerializer
    queryset = Orders.objects.all()
    success_response_message = "Order Updated Successfully."
