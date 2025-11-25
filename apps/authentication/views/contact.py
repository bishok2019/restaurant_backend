from apps.authentication.serializers.contact_us import (
    ContactUsCreateSerializer,
    ContactUsGetSerializer,
)

from apps.authentication.filters.user import ContactUsFilter
from apps.authentication.models.user_profile import ContactUs
from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
)


class ContactUsCreateView(CustomGenericCreateView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsCreateSerializer
    success_response_message = "Message sent successfully."
    permission_classes = []


class ContactUsListView(CustomGenericListView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsGetSerializer
    success_response_message = "Contact messages fetched successfully."
    search_fields = ["name", "email"]
    filterset_class = ContactUsFilter
