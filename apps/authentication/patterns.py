from django.urls import path

from apps.authentication.views.permissions import (
    PermissionsCategoryListView,
    PermissionsListDropdownView,
    PermissionsListView,
    RolesCreateView,
    RolesListDropdownView,
    RolesListView,
    RolesRetrieveView,
    RolesUpdateView,
)
from apps.authentication.views.users import (
    ChangeUserPasswordView,
    UpdateUserPasswordView,
    UserCreateView,
    UserListView,
    UserRetrieveView,
    UserUpdateView,
)

######################################################
######################## Users #######################
######################################################
user_patterns = [
    path("list", UserListView.as_view(), name="user_list"),
    path("create", UserCreateView.as_view(), name="user_create"),
    path("retrieve/<int:pk>", UserRetrieveView.as_view(), name="user_retrieve"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    path(
        "change-password",
        ChangeUserPasswordView.as_view(),
        name="change_password",
    ),
    path(
        "update-password/<int:pk>",
        UpdateUserPasswordView.as_view(),
        name="update_password",
    ),
]
roles = [
    path("create", RolesCreateView.as_view(), name="roles_create"),
    path(
        "retrieve/<int:pk>",
        RolesRetrieveView.as_view(),
        name="roles_retrieve",
    ),
    path(
        "update/<int:pk>",
        RolesUpdateView.as_view(),
        name="roles_update",
    ),
    path("list", RolesListView.as_view(), name="roles_list"),
    path(
        "list/dropdown",
        RolesListDropdownView.as_view(),
        name="roles_list_dropdown",
    ),
]
permission = [
    path(
        "permission/list",
        PermissionsListView.as_view(),
        name="permission_list",
    ),
    path(
        "permission/list/dropdown",
        PermissionsListDropdownView.as_view(),
        name="permission_list_dropdown",
    ),
    path(
        "permission-category/list",
        PermissionsCategoryListView.as_view(),
        name="permission_category_list",
    ),
]
