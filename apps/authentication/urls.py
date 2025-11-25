from django.urls import include, path

from apps.authentication.views.contact import ContactUsCreateView, ContactUsListView
from apps.authentication.views.forget_password import (
    ChangePasswordWithOtpView,
    ForgetPasswordView,
)
from apps.authentication.views.users import (
    CustomUserProfileGetView,
    CustomUserProfileUpdateView,
    GetAllProfileListApiView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    UserDeleteView,
    UserSignUpAPIView,
)

from .patterns import permission, roles, user_patterns

users_and_permissions = [
    path("users/", include(user_patterns)),
    path("role/", include(roles)),
    path("permissions/", include(permission)),
]
urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("refresh-token", RefreshTokenView.as_view(), name="token_refresh"),
    path("", include(users_and_permissions)),
    path("user-delete/<int:pk>", UserDeleteView.as_view(), name="user_delete"),
    path(
        "update-profile",
        CustomUserProfileUpdateView.as_view(),
        name="update_profile",
    ),
    path(
        "get-user-profile", CustomUserProfileGetView.as_view(), name="get_user_profile"
    ),
    path(
        "get-all-profile-list",
        GetAllProfileListApiView.as_view(),
        name="get_all_profile_list",
    ),
    path("forget-password", ForgetPasswordView.as_view(), name="forget_password"),
    path(
        "change-password-otp",
        ChangePasswordWithOtpView.as_view(),
        name="change_password",
    ),
    path("public-sign-up", UserSignUpAPIView.as_view(), name="public_sign_up"),
    path("contact-us/create", ContactUsCreateView.as_view(), name="contact_us_create"),
    path("contact-us/list", ContactUsListView.as_view(), name="contact_us_list"),
]
