from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from base.views.generic_views import (
    CustomAPIResponse,
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..filters.user import UserFilters
from ..models import CustomUser, UserProfile
from ..permissions.permissions import (
    IsAuthenticated,
)
from ..serializers import (
    ChangePasswordSerializer,
    CustomUserCreateSerializer,
    CustomUserRetrieveSerializer,
    CustomUserUpdateSerializer,
    GetAllProfileUserSerializer,
    GetUserProfileSerializer,
    LoginSerializer,
    LogoutSerializer,
    UpdateUserProfileSerializer,
    UserListSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "Logged out successfully."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Logout failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "timestamp": now,
        }
        if serializer.is_valid():
            return Response(
                {
                    "success": True,
                    "message": "Logged in successfully.",
                    "meta_data": meta_data,
                    **serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "success": False,
                "message": "Invalid Credentials.",
                "meta_data": meta_data,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class RefreshTokenView(TokenRefreshView):
    permission_classes = []


class UserCreateView(CustomGenericCreateView):
    serializer_class = CustomUserCreateSerializer
    queryset = User.objects.all()


class UserUpdateView(CustomGenericUpdateView):
    serializer_class = CustomUserUpdateSerializer
    queryset = User.objects.all()
    success_response_message = "User updated successfully."


class UserRetrieveView(CustomGenericRetrieveView):
    serializer_class = CustomUserRetrieveSerializer
    queryset = User.objects.all()
    success_response_message = "Users retrieved successfully."


class UserListView(CustomGenericListView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    success_response_message = "Users fetched successfully."
    filterset_class = UserFilters
    search_fields = [
        "username",
        "email",
        "palika",
        "tole",
    ]


class ChangeUserPasswordView(CustomGenericUpdateView):
    serializer_class = ChangePasswordSerializer
    success_response_message = "Password changed successfully."
    queryset = User.objects.all()

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        user = self.request.user
        self.kwargs["user"] = user
        return user


class UpdateUserPasswordView(CustomGenericUpdateView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    success_response_message = "Password updated successfully."
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        kwargs = self.kwargs
        user_id = kwargs["pk"]
        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            message = "User not found."
            return CustomAPIResponse.custom_error_response(message=message)
        kwargs["user"] = user
        return user


class UserDeleteView(APIView):
    permission_classes = []
    # serializer_class = UserDeleteSerializer
    queryset = CustomUser.objects.all()

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = False
        user.save()

        # serializer = self.serializer_class(user)
        return Response(
            {"message": "User deleted successfully.", "data": None},
            status=status.HTTP_200_OK,
        )


class CustomUserProfileGetView(generics.GenericAPIView):
    serializer_class = GetUserProfileSerializer
    permission_classes = [IsAuthenticated]
    success_response_message = "User profile retrieved successfully."
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profile = None
        try:
            user_profile = user.profile
        except Exception:
            pass

        if not user_profile:
            return Response(
                {"profile": "User profile does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if not hasattr(user, "profile"):
        #     return Response(
        #         {"profile": "User profile does not exist."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        serializer = self.serializer_class(user, context={"request": request})

        return CustomAPIResponse.custom_success_response(
            data=serializer.data, message=self.success_response_message
        )


class CustomUserProfileUpdateView(CustomGenericUpdateView):
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    success_response_message = "User profile updated successfully."
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        from rest_framework import serializers

        context = super().get_serializer_context()
        user = self.get_object()

        profile = UserProfile.objects.filter(user_id=user.id).first()
        if not profile:
            raise serializers.ValidationError(
                {
                    "profile": "User profile does not exist.",
                }
            )

        context["profile_obj"] = profile
        return context


class GetAllProfileListApiView(CustomGenericListView):
    serializer_class = GetAllProfileUserSerializer
    queryset = UserProfile.objects.all()
    search_fields = [
        "user__username",
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request

        if request.user.is_authenticated:
            try:
                current_profile = request.user.profile

                # IDs of users current_profile has blocked
                blocked_user_ids = current_profile.blocked_users.values_list(
                    "user_id", flat=True
                )

                # IDs of users who have blocked current_profile
                blocked_by_user_ids = current_profile.blocked_by.values_list(
                    "user_id", flat=True
                )

                # Exclude profiles of blocked/blocking users
                qs = qs.exclude(user__id__in=blocked_user_ids).exclude(
                    user__id__in=blocked_by_user_ids
                )

                # Optional: Also exclude current user's own profile
                qs = qs.exclude(user=request.user)
            except Exception:
                pass

        return qs


class UserSignUpAPIView(CustomGenericCreateView):
    serializer_class = UserSignUpSerializer
    permission_classes = []

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            message = self._get_message(data=errors)
            if message:
                return CustomAPIResponse.custom_error_response(message=message)
        serializer.save()
        # response = user.tokens(request)
        return CustomAPIResponse.custom_success_response(
            data=serializer.data,
            message="Signup successful",
        )
