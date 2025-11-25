from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models.user_profile import OTP
from apps.authentication.models.users import CustomUser
from apps.authentication.serializers.forget_password_otp import (
    ChangePasswordWithOtpSerializer,
    ForgetPasswordOtpSerializer,
)
from base.views.generic_views import CustomGenericCreateView


class ForgetPasswordView(CustomGenericCreateView):
    serializer_class = ForgetPasswordOtpSerializer
    permission_classes = []
    success_response_message = "OTP sent successfully."
    queryset = OTP.objects.all()


class ChangePasswordWithOtpView(APIView):
    permission_classes = []
    serializer_class = ChangePasswordWithOtpSerializer

    def post(self, request):
        serializer = ChangePasswordWithOtpSerializer(data=request.data)
        if serializer.is_valid():
            otp_value = serializer.validated_data["otp"]

            # # Looking for the otp
            otp_instance = OTP.objects.filter(otp=otp_value).last()
            if not otp_instance:
                return Response(
                    {"otp": ["Invalid or expired OTP."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Find the user associated with the OTP
            user = CustomUser.objects.filter(
                email__iexact=otp_instance.email, username__iexact=otp_instance.code
            ).first()
            if not user:
                return Response(
                    {"detail": "User not found for this OTP."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the user's password
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            # Delete the OTP after successful password update
            otp_instance.delete(hard=True)

            return Response(
                {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
