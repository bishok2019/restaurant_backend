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
)


class KitchenCategoryListApiView(CustomGenericListView):
    serializer_class = Kitchen_CategoryListSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCategoryCreateApiView(CustomGenericListView):
    serializer_class = Kitchen_CategoryCreateSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCategoryRetrieveApiView(CustomGenericListView):
    serializer_class = Kitchen_CategoryListSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCategoryUpdateApiView(CustomGenericListView):
    serializer_class = Kitchen_CategoryUpdateSerializer
    queryset = Kitchen_Category.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenListApiView(CustomGenericListView):
    serializer_class = KitchenListSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenCreateApiView(CustomGenericListView):
    serializer_class = KitchenListSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenRetrieveApiView(CustomGenericListView):
    serializer_class = KitchenListSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Fetched Successfully"


class KitchenUpdateApiView(CustomGenericListView):
    serializer_class = KitchenListSerializer
    queryset = Kitchen.objects.all()
    success_response_message = "Kitchen Fetched Successfully"
