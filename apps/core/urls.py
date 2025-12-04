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
    MenuCreateApiView,
    MenuItemCreateApiView,
    MenuItemListApiView,
    MenuItemRetrieveApiView,
    MenuItemUpdateApiView,
    MenuListApiView,
    MenuRetrieveApiView,
    MenuUpdateApiView,
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

menu_patterns = [
    path("create", MenuCreateApiView.as_view(), name="menu-create"),
    path("list", MenuListApiView.as_view(), name="menu-list"),
    path("retrieve/<int:pk>", MenuRetrieveApiView.as_view(), name="menu-retrieve"),
    path("update/<int:pk>", MenuUpdateApiView.as_view(), name="menu-update"),
]
menu_item_patterns = [
    path("list", MenuItemListApiView.as_view(), name="menu-item-menu-list"),
    path("create", MenuItemCreateApiView.as_view(), name="menu-item-menu-create"),
    path(
        "retrieve/<int:pk>",
        MenuItemRetrieveApiView.as_view(),
        name="menu-item-retrieve",
    ),
    path(
        "update/<int:pk>",
        MenuItemUpdateApiView.as_view(),
        name="menu-item-update",
    ),
]


kitchen_patterns = [
    path(
        "category/create",
        KitchenCategoryCreateApiView.as_view(),
        name="kitchen-category-create",
    ),
    path(
        "category/list",
        KitchenCategoryListApiView.as_view(),
        name="kitchen-category-list",
    ),
    path(
        "category/retrieve/<int:pk>",
        KitchenCategoryRetrieveApiView.as_view(),
        name="kitchen-category-retrieve",
    ),
    path(
        "category/update/<int:pk>",
        KitchenCategoryUpdateApiView.as_view(),
        name="kitchen-category-update",
    ),
    path("create", KitchenCreateApiView.as_view(), name="kitchen-create"),
    path("list", KitchenListApiView.as_view(), name="kitchen-list"),
    path(
        "retrieve/<int:pk>", KitchenRetrieveApiView.as_view(), name="kitchen-retrieve"
    ),
    path("update/<int:pk>", KitchenUpdateApiView.as_view(), name="kitchen-update"),
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
    path("kitchen/", include(kitchen_patterns)),
    path("menu/", include(menu_patterns)),
    path("menu/items/", include(menu_item_patterns)),
]
