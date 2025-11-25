from django.urls import path

from . import views

urlpatterns = [
    path("list", views.APILogsListView.as_view(), name="api_logs_list"),
    path(
        "retrieve/<int:pk>",
        views.APILogsRetrieveView.as_view(),
        name="api_logs_retrieve",
    ),
]
