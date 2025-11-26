from .contact import ContactUsCreateView, ContactUsListView
from .forget_password import ChangePasswordWithOtpView, ForgetPasswordView
from .permissions import (
    PermissionsCategoryListView,
    PermissionsListDropdownView,
    PermissionsListView,
    RolesCreateView,
    RolesListDropdownView,
    RolesListView,
    RolesRetrieveView,
    RolesUpdateView,
)
from .users import (
    ChangePasswordView,
    ChangeUserPasswordView,
    CustomUserProfileGetView,
    CustomUserProfileUpdateView,
    GetAllProfileListApiView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    UpdateUserPasswordView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserRetrieveView,
    UserSignUpAPIView,
    UserUpdateView,
)

__all__ = [
    # contact
    "ContactUsCreateView",
    "ContactUsListView",
    # forget_password
    "ForgetPasswordView",
    "ChangePasswordWithOtpView",
    # permissions
    "PermissionsListView",
    "PermissionsListDropdownView",
    "PermissionsCategoryListView",
    "RolesListView",
    "RolesListDropdownView",
    "RolesRetrieveView",
    "RolesCreateView",
    "RolesUpdateView",
    # users
    "ChangePasswordView",
    "LogoutView",
    "LoginView",
    "RefreshTokenView",
    "UserCreateView",
    "UserUpdateView",
    "UserRetrieveView",
    "UserListView",
    "ChangeUserPasswordView",
    "UpdateUserPasswordView",
    "UserDeleteView",
    "CustomUserProfileGetView",
    "CustomUserProfileUpdateView",
    "GetAllProfileListApiView",
    "UserSignUpAPIView",
]
