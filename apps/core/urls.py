from django.urls import include, path

from .views import (
    EmployeeCreateApiView,
    EmployeeListApiView,
    EmployeeRetrieveApiView,
    EmployeeUpdateApiView,
    KitchenCategoryCreateApiView,
    KitchenCategoryListApiView,
    KitchenCategoryRetrieveApiView,
    KitchenCategoryUpdateApiView,
    KitchenCreateApiView,
    KitchenListApiView,
    KitchenRetrieveApiView,
    KitchenUpdateApiView,
    OrdersCreateApiView,
    OrdersItemCreateApiView,
    OrdersItemListApiView,
    OrdersItemRetrieveApiView,
    OrdersItemUpdateApiView,
    OrdersListApiView,
    OrdersRetrieveApiView,
    OrdersUpdateApiView,
)

employee_patterns = [
    path("create", EmployeeCreateApiView.as_view(), name="employee-create"),
    path("list", EmployeeListApiView.as_view(), name="employee-create"),
    path(
        "retrieve/<int:pk>", EmployeeRetrieveApiView.as_view(), name="employee-create"
    ),
    path("update/<int:pk>", EmployeeUpdateApiView.as_view(), name="employee-create"),
]

orders_patterns = [
    path("create", OrdersCreateApiView.as_view(), name="orders-create"),
    path("list", OrdersListApiView.as_view(), name="orders-create"),
    path("retrieve/<int:pk>", OrdersRetrieveApiView.as_view(), name="orders-create"),
    path("update/<int:pk>", OrdersUpdateApiView.as_view(), name="orders-create"),
]

orders_items_patterns = [
    path("create", OrdersItemCreateApiView.as_view(), name="orders-item-create"),
    path("list", OrdersItemListApiView.as_view(), name="orders-item-create"),
    path(
        "retrieve/<int:pk>",
        OrdersItemRetrieveApiView.as_view(),
        name="orders-item-create",
    ),
    path(
        "update/<int:pk>", OrdersItemUpdateApiView.as_view(), name="orders-item-create"
    ),
]
urlpatterns = [
    path("orders/", include(orders_patterns)),
    path("order_items/", include(orders_items_patterns)),
    path("employee/", include(employee_patterns)),
]
