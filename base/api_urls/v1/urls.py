"""
Every upcoming apps' url will route through this urls.
On doing so, the API will be automatically documented
in swagger.
"""

from django.urls import include, path

urlpatterns = [
    path("auth-app/", include("apps.authentication.urls")),
    path("api-logs-app/", include("apps.api_logs.urls")),
    path("location-app/", include("apps.location.urls")),
    path("core-app/", include("apps.core.urls")),
]
