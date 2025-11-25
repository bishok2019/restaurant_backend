from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import serializers

from apps.authentication.models.user_profile import UserProfile
from apps.authentication.models.users import CustomUser
from base.serializers import AbstractBaseModelSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # model = UserProfile
        fields = ["full_name", "phone"]


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "user_type", "is_active", "user_profile"]


class SignupSerializer(AbstractBaseModelSerializer):
    full_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=True)
    # user_type = serializers.ChoiceField(
    #     choices=CustomUser.USER_TYPES, default="retailer"
    # )

    class Meta:
        model = CustomUser
        fields = ["email", "user_type", "full_name", "phone"]

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        # if UserProfile.objects.filter(phone=value).exists():
        #     raise serializers.ValidationError(
        #         "A user with this phone number already exists."
        #     )
        return value

    def validate_user_type(self, value):
        if value not in dict(CustomUser.USER_TYPES):
            raise serializers.ValidationError(
                f"Invalid User Type! Choices are : {dict(CustomUser.USER_TYPES)}"
            )
        return value

    def create(self, validated_data):
        # Get user ID from request context
        user_id = self.context["request"].user.id
        validated_data["created_by"] = user_id
        validated_data["modified_by"] = user_id

        # full_name = validated_data.pop("full_name")
        # phone = validated_data.pop("phone")

        password = get_random_string(8)
        user = CustomUser.objects.create(
            email=validated_data["email"],
            user_type=validated_data["user_type"],
            password=make_password(password),
            is_active=True,
            is_superuser=False,
            is_staff=False,
            is_admin=False,
        )
        # user_profile = UserProfile.objects.create(
        #     user=user,
        #     bio="",
        # )
        UserProfile.objects.create(
            user=user,
            bio="",
        )

        # create UserProfile instance
        # UserProfile.objects.create(user=user, full_name=full_name, phone=phone)

        # Store password to send via email later (can be reused on VIEW to send raw password)
        user.raw_password = password

        return user
