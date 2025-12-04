from base.views.generic_views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import Kitchen, Kitchen_Category
from ..serializers import (
    Kitchen_CategoryCreateSerializer,
    Kitchen_CategoryListSerializer,
    Kitchen_CategoryRetrieveSerializer,
    Kitchen_CategoryUpdateSerializer,
    KitchenCreateSerializer,
    KitchenListSerializer,
    KitchenRetrieveSerializer,
    KitchenUpdateSerializer,
)


class KitchenCategoryListApiView(CustomGenericListView):
    serializer_class = Kitchen_CategoryListSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCategoryCreateApiView(CustomGenericCreateView):
    serializer_class = Kitchen_CategoryCreateSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Created Successfully"


class KitchenCategoryRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = Kitchen_CategoryRetrieveSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Retrieved Successfully"


class KitchenCategoryUpdateApiView(CustomGenericUpdateView):
    serializer_class = Kitchen_CategoryUpdateSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Updated Successfully"


class KitchenListApiView(CustomGenericListView):
    serializer_class = KitchenListSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCreateApiView(CustomGenericCreateView):
    serializer_class = KitchenCreateSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Created Successfully"


class KitchenRetrieveApiView(CustomGenericRetrieveView):
    serializer_class = KitchenRetrieveSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Retrieved Successfully"


class KitchenUpdateApiView(CustomGenericUpdateView):
    serializer_class = KitchenUpdateSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Updated Successfully"
