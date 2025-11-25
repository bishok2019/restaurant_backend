from apps.authentication.models.perms import CustomPermission, Roles
from apps.authentication.models.user_profile import UserProfile
from apps.authentication.models.users import CustomUser
from apps.authentication.serializers.permissions import RolesListSerializerDropdown
from apps.authentication.utils import refresh_permissions_cache
from apps.location.models import District
from base.serializers import BaseModelSerializer, serializers

from ...location.serializers import DistrictSerializer


class CustomUserCreateSerializer(BaseModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Roles.objects.all(),
        required=False,
    )
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomPermission.objects.all(),
        required=False,
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        required=False,
    )
    # palika = serializers.PrimaryKeyRelatedField(
    #     queryset=Palika.objects.all(),
    #     required=False,
    # )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "birth_date",
            "district",
            "palika",
            "ward_no",
            "tole",
            "mobile_no",
            "photo",
            "roles",
            "permissions",
            "is_active",
            "password",
            "user_type",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "username": {"required": False},
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate(self, attrs):
        if not attrs.get("username", None):
            attrs["username"] = attrs["email"]
        return super().validate(attrs)

    def create(self, validated_data):
        m2m_fields = {
            "roles": validated_data.pop("roles", []),
            "permissions": validated_data.pop("permissions", []),
        }

        user = super().create(validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        for field, values in m2m_fields.items():
            getattr(user, field).set(values)
        refresh_permissions_cache(user)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class CustomUserRetrieveSerializer(BaseModelSerializer):
    district = DistrictSerializer(read_only=True)
    roles = RolesListSerializerDropdown(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "user_type",
            "gender",
            "birth_date",
            "district",
            "palika",
            "ward_no",
            "tole",
            "mobile_no",
            "photo",
            "roles",
            "permissions",
            "is_active",
            "is_superuser",
            "is_staff",
            "is_admin",
        ]


class CustomUserUpdateSerializer(BaseModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Roles.objects.all(),
        required=False,
    )
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomPermission.objects.all(),
        required=False,
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = "__all__"


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "photo",
            "is_active",
            "is_superuser",
            "is_admin",
            "is_staff",
        ]


class UserProfileListSerializer(BaseModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "bio",
        ]


class GetUserListForAllProfileListSerializer(BaseModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "photo",
            "email",
        ]


class GetAllProfileUserSerializer(BaseModelSerializer):
    user = GetUserListForAllProfileListSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
        ]


class GetUserProfileSerializer(BaseModelSerializer):
    user = GetUserListForAllProfileListSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
        ]


class ProfileForUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "bio",
        ]


class UpdateUserProfileSerializer(BaseModelSerializer):
    profile = ProfileForUpdateSerializer()

    class Meta:
        model = CustomUser
        fields = [
            # "id",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "photo",
            "username",
            "profile",
        ]

        extra_kwargs = {
            "username": {"read_only": True},
            "full_name": {"read_only": True},
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        user_instance = super().update(instance, validated_data)

        profile_obj = self.context.get("profile_obj")
        if not profile_obj:
            raise serializers.ValidationError(
                "Profile object not found in serializer context."
            )

        for attr, value in profile_data.items():
            setattr(profile_obj, attr, value)

        profile_obj.save()
        return user_instance


class UserListSerializer(BaseModelSerializer):
    profile = UserProfileListSerializer(required=False, read_only=True)
    roles = RolesListSerializerDropdown(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "photo",
            "is_active",
            "is_superuser",
            "is_admin",
            "is_staff",
            "profile",
            "is_blocked",
            "user_type",
            "mobile_no",
            "roles",
        ]


class UserSignUpSerializer(BaseModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "birth_date",
            "palika",
            "district",
            "ward_no",
            "tole",
            "mobile_no",
            "photo",
        ]

    def validate(self, data):
        username = data["username"]
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                {"username": "User already exists. Please sign in."}
            )

        email = data.get("email")
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data["username"] = validated_data["username"].lower()

        user = CustomUser(**validated_data)
        user.set_password(password)
        user.user_type = "public"
        user.is_active = True
        user.save()

        UserProfile.objects.create(user=user)

        return user
