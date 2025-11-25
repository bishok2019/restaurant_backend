from apps.authentication.models.user_profile import ContactUs
from base.serializers import BaseModelSerializer


class ContactUsCreateSerializer(BaseModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


class ContactUsGetSerializer(BaseModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
