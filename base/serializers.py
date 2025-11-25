from collections import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from base.models import ad_to_bs_converter

from .exceptions import APIError

User = get_user_model()


# from rest_framework.exceptions import ErrorDetail
class ExcludeFieldsForMain:
    exclude = []  # We need all data in main


class ReadOnlyFields:
    read_only = [
        "created_by",
        "created_at",
        "created_at_bs",
        "updated_at",
        "modified_by",
        "deleted_at",
        "device_type",
        "os_type",
    ]


class ExcludeFields:
    exclude = [
        "created_by",
        "created_at",
        "created_at_bs",
        "updated_at",
        "modified_by",
        "deleted_at",
        "device_type",
        "os_type",
    ]


class ActionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", [])
        include_fields = kwargs.pop("include_fields", [])
        super().__init__(*args, **kwargs)
        for field_name in exclude_fields:
            self.fields.pop(field_name, None)

        # Include only specified fields
        if include_fields:
            new_fields = {
                field_name: self.fields[field_name] for field_name in include_fields
            }
            self.fields = new_fields

    def _assign_os_device(self, attrs):
        request = self.context.get("request", None)
        device_type = {
            "mobile": request.user_agent.is_mobile,
            "pc": request.user_agent.is_pc,
            "tablet": request.user_agent.is_tablet,
            "other": request.user_agent.is_tablet,
        }
        os_ = request.user_agent.os.family.lower()
        os_type_ = os_.split()[0]
        os_type = {
            "windows": os_type_ == "windows",
            "ios": os_type_ == "ios",
            "android": os_type_ == "android",
            "mac": os_type_ == "mac",
            "linux": os_type_ == "linux",
            "other": os_type_ == "other",
        }

        true_os = next((key for key, value in os_type.items() if value), "other")
        true_device = next(
            (key for key, value in device_type.items() if value), "other"
        )

        attrs["device_type"] = true_device
        attrs["os_type"] = true_os
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request_data = self.context.get("request")
        validated_data.pop("id", None)
        if not request_data:
            raise serializers.ValidationError(
                {
                    "message": "Invalid request. `request` needs to be passed "
                    "while creating the data"
                }
            )
        if not settings.DISABLED_AUTHENTICATION:
            user_id = None
            try:
                user_id = self.context.get("request").user.id
            except Exception:
                raise serializers.ValidationError(
                    {"message": "Invalid request. Invalid user."}
                )
            if user_id:
                validated_data["created_by"] = user_id
                validated_data["modified_by"] = user_id
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        request_data = self.context.get("request")
        if not request_data:
            raise serializers.ValidationError(
                {
                    "message": "Invalid request. `request` needs to be passed "
                    "while updating the data"
                }
            )

        if not settings.DISABLED_AUTHENTICATION:
            user_id = None
            try:
                user_id = self.context.get("request").user.id
            except Exception:
                raise serializers.ValidationError(
                    {"message": "Invalid request. Invalid user."}
                )

            if not user_id:
                raise serializers.ValidationError(
                    {
                        "message": "Failed to update the instance",
                        "detail": "Public user can not update the data",
                    }
                )
            validated_data["modified_by"] = user_id
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)

        if "created_by" in self.fields:
            if instance.created_by:
                if instance.created_by >= 1 and "created_by" in self.fields:
                    repr["created_by"] = ActionUserSerializer(
                        User.objects.get(id=instance.created_by)
                    ).data
        if "modified_by" in self.fields:
            if instance.modified_by:
                if instance.modified_by >= 1 and "modified_by" in self.fields:
                    repr["modified_by"] = ActionUserSerializer(
                        User.objects.get(id=instance.modified_by)
                    ).data

        return repr

    @transaction.atomic
    def _update_one_to_one(
        self,
        related_field,
        related_data,
        RelatedModel,
        data,
        unique_instances_check_and_delete=False,
    ):
        """
        Update a one-to-one related object if data is provided.
        """
        if not data:
            return
        data[related_field] = related_data
        # if self.for_branch:
        #     data["branch"] = related_data.branch

        if unique_instances_check_and_delete:
            pk_list_to_not_delete = [_["id"] for _ in data if _.get("id", None)]
            needs_to_delete_data = RelatedModel.all_objects.exclude(
                id__in=pk_list_to_not_delete
            )
            needs_to_delete_data.delete()
        pk = data.pop("id", None)
        if pk:
            filter_data = {related_field: related_data, "pk": pk}
        else:
            filter_data = {related_field: related_data}

        one_to_one_obj = RelatedModel.objects.filter(**filter_data).first()

        if not one_to_one_obj:
            data.pop("id", None)
            RelatedModel.objects.create(**data)
        else:
            for attr, value in data.items():
                setattr(one_to_one_obj, attr, value)
            one_to_one_obj.save()

    @transaction.atomic
    def _update_foreign_keys(
        self,
        related_field,
        related_data,
        RelatedModel,
        data_list,
        file_instance=False,
        unique_instances_check_and_delete=False,
    ):
        """
        Handle updates and creation for foreign key relations.
        """

        if not data_list:
            return

        existing_ids = []
        update_instances = []
        new_instances = []

        if unique_instances_check_and_delete:
            pk_list_to_delete = [
                data["id"] for data in data_list if data.get("id", None)
            ]
            needs_to_delete_data = RelatedModel.all_objects.exclude(
                id__in=pk_list_to_delete
            )
            needs_to_delete_data.delete()

        for data in data_list:
            data[related_field] = related_data
            pk = data.pop("id", None)
            if pk:
                try:
                    filter_data = {
                        related_field: related_data,
                        "pk": pk,
                    }
                    instance = RelatedModel.objects.get(**filter_data)
                    if instance:
                        for attr, value in data.items():
                            setattr(instance, attr, value)
                        update_instances.append(instance)
                        existing_ids.append(pk)
                except Exception:
                    pass
            else:
                new_instances.append(RelatedModel(**data))

        # Bulk update existing objects
        if update_instances:
            if file_instance:
                for _ in update_instances:
                    _.save()
            else:
                # Imp : data.keys() works because all the iterated data have same key values
                RelatedModel.objects.bulk_update(update_instances, fields=data.keys())

        # Bulk create new objects
        if new_instances:
            RelatedModel.objects.bulk_create(new_instances, ignore_conflicts=True)

    @transaction.atomic
    def _bulk_create_foreign_keys(
        self, related_field, related_data, RelatedModel, data_list, file_instance=False
    ):
        # related_data is a foreign key
        """
        Handle Bulk creation for foreign key relations (Reverse Relations).
        """
        if not data_list:
            return

        bulk_created_objs = []

        if file_instance:
            for data in data_list:
                data.pop("id", None)
                data_with_related_field = {
                    related_field: related_data,
                    "created_by": related_data.created_by,
                    "created_at_bs": ad_to_bs_converter(timezone.now()),
                    "modified_by": related_data.modified_by,
                    **data,
                }

                if self.for_branch:
                    data_with_related_field.update({"branch": related_data.branch})

                created_obj = RelatedModel.objects.create(**data_with_related_field)
                bulk_created_objs.append(created_obj.id)
        else:
            to_bulk_create = []
            for data in data_list:
                # Use Set Attribute to use ForeignKey related_field string useable
                data.pop("id", None)

                data_with_related_field = {
                    related_field: related_data,
                    "created_by": related_data.created_by,
                    "created_at_bs": ad_to_bs_converter(timezone.now()),
                    "modified_by": related_data.modified_by,
                    **data,
                }
                if self.for_branch:
                    data_with_related_field.update({"branch": related_data.branch})
                obj = RelatedModel(**data_with_related_field)
                setattr(obj, related_field, related_data)  # Set ForeignKey as an object
                to_bulk_create.append(obj)

            bulk_created_obj = RelatedModel.objects.bulk_create(to_bulk_create)

            if bulk_created_obj:
                bulk_created_objs.extend([_.id for _ in bulk_created_obj])

        return bulk_created_objs

    @property
    def errors(self):
        formatted_errors = OrderedDict()

        all_errors = super().errors
        if not all_errors:
            return ReturnDict(formatted_errors, serializer=self)

        fields = self.fields  # caching fields
        required_msg = "This field is required."

        for field_name, field_errors in all_errors.items():
            # Skip empty errors immediately
            if not field_errors:
                continue

            # Handle non-list errors directly
            if not isinstance(field_errors, list):
                formatted_errors[field_name] = field_errors
                continue

            # Get field type once
            field = fields.get(field_name)

            # Handle non-ListSerializer fields directly
            if not isinstance(field, ListSerializer):
                formatted_errors[field_name] = field_errors
                continue

            # Handle required field error - most common case first
            if len(field_errors) == 1 and field_errors[0] == required_msg:
                formatted_errors[field_name] = field_errors
                continue

            indexed_errors = {
                idx: (
                    error
                    if isinstance(error, dict)
                    else {"non_field_errors": [str(error).capitalize()]}
                )
                for idx, error in enumerate(field_errors)
                if error
            }

            if indexed_errors:
                formatted_errors[field_name] = indexed_errors

        return ReturnDict(formatted_errors, serializer=self)

    @property
    def exception_class(self):
        return APIError

    def raise_exception(
        self,
        errors={},
    ):
        if not errors:
            raise ValueError("`errors` dict is required to raise a exception.")
        raise self.exception_class(errors)

    def get_request(self):
        request = self.context.get("request", None)
        if not request:
            self.raise_exception(
                {"request": "Request needs to be passed to the serializer"}
            )
            return None, None
        return request, request.method.lower()

    def validate_update(self, attrs):
        return attrs

    def validate_create(self, attrs):
        return attrs

    def init_empty_dict_of_errors(self):
        # Initialize a empty dict for errors
        self.empty_dict_of_errors = {}

    def custom_errors_generator(
        self, error_dict, error_key, error_value: dict, parent_key
    ):
        """
        appends the given errors into the empt_dict_of_errors
        """
        if parent_key not in self.empty_dict_of_errors:
            self.empty_dict_of_errors[parent_key] = {}
        index = str(error_key)
        self.empty_dict_of_errors[parent_key][index] = error_value

    def raise_if_validation_errors(self):
        """
        This has to be called everytime we generate and stack errors and if the  dict of  errors is not empty then raise exception
        """

        if self.empty_dict_of_errors:
            keys_to_remove = [
                key for key, value in self.empty_dict_of_errors.items() if not value
            ]
            for key in keys_to_remove:
                del self.empty_dict_of_errors[key]
            self.raise_exception(errors=self.empty_dict_of_errors)


class AbstractBaseModelSerializer(serializers.ModelSerializer):
    """
    this base serializer sets the `created_by` and `modified_by` fields
    from the JWT token in the request.
    """

    def create(self, validated_data):
        user_id = self.context["request"].user.id
        print("user id : ", user_id, self.context["request"].user)
        validated_data["created_by"] = user_id
        validated_data["modified_by"] = user_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user_id = self.context["request"].user.id
        validated_data["modified_by"] = user_id
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if instance.created_by >= 1 and "created_by" in self.fields:
            repr["created_by"] = ActionUserSerializer(
                User.objects.get(id=instance.created_by)
            ).data
        if instance.modified_by >= 1 and "modified_by" in self.fields:
            repr["modified_by"] = ActionUserSerializer(
                User.objects.get(id=instance.modified_by)
            ).data
        return repr

    class Meta:
        abstract = True
