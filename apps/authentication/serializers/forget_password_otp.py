from random import randint

from django.conf import settings
from django.core.mail import send_mail

from apps.authentication.models.user_profile import OTP
from apps.authentication.models.users import CustomUser
from base.serializers import BaseModelSerializer, serializers


def send_otp(email, otp):
    subject = "Your One-Time Password (OTP)"
    message = f"Your OTP code is: {otp}\nPlease use this to verify your account. It will expire soon."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


class ForgetPasswordOtpSerializer(BaseModelSerializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    class Meta:
        model = OTP
        fields = ["email", "code"]
        validators = []

    def validate(self, attrs):
        email = attrs["email"]
        username = attrs["code"]

        user = CustomUser.objects.filter(username__iexact=username).first()
        if not user:
            raise serializers.ValidationError({"username": "Username does not exist."})

        if user.email:
            if user.email != email:
                raise serializers.ValidationError(
                    {"email": "This email does not match."}
                )
        else:
            # Patch missing email
            user.email = email
            user.save(update_fields=["email"])

        return attrs

    def create(self, validated_data):
        username = validated_data["code"]
        email = validated_data["email"]
        otp = str(randint(100000, 999999))

        # Check if an OTP already exists for this email + code
        otp_instance = OTP.objects.filter(
            email__iexact=email, code__iexact=username
        ).first()

        if otp_instance:
            # Update the existing OTP instead of creating a new one
            otp_instance.otp = otp
            otp_instance.save(update_fields=["otp"])
        else:
            # Create a fresh OTP record
            otp_instance = OTP.objects.create(
                code=username,
                email=email,
                otp=otp,
            )

        # Send OTP after create/update
        send_otp(email, otp)

        return otp_instance


# class ChangePasswordWithOtpSerializer(BaseModelSerializer):
#     otp = serializers.CharField(required=True)
#     new_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ["otp", "new_password"]

#     def validate_otp(self, value):
#         if not OTP.objects.filter(otp=value).exists():
#             raise serializers.ValidationError("Invalid OTP.")
#         return value

#     def update(self, instance, validated_data):
#         instance.set_password(validated_data["new_password"])
#         instance.save()
#         return instance


class ChangePasswordWithOtpSerializer(BaseModelSerializer):
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["otp", "new_password"]

    def validate_otp(self, value):
        otp_instance = OTP.objects.filter(otp=value).first()
        if not otp_instance:
            raise serializers.ValidationError("Invalid OTP.")
        self.context["otp_instance"] = otp_instance
        return value

    def update(self, instance, validated_data):
        new_password = validated_data["new_password"]
        instance.set_password(new_password)
        instance.save()

        # OTP after use
        # otp_instance = self.context.get('otp_instance')
        # if otp_instance:
        #     otp_instance.delete()

        return instance
