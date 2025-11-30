from base.serializers import BaseModelSerializer, ExcludeFields, serializers

from ..models import Employee


class EmployeeListSerializer(BaseModelSerializer):
    class Meta:
        model = Employee
        exclude = ExcludeFields.exclude


class EmployeeCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Employee
        exclude = ExcludeFields.exclude


class EmployeeRetrieveSerializer(BaseModelSerializer):
    class Meta:
        model = Employee
        exclude = ExcludeFields.exclude


class EmployeeUpdateSerializer(BaseModelSerializer):
    class Meta:
        model = Employee
        exclude = ExcludeFields.exclude
