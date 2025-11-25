from django.urls import path

from . import views

urlpatterns = [
    path("provinces/list", views.ProvinceListView.as_view(), name="province_list"),
    path("districts/list", views.DistrictListView.as_view(), name="district_list"),
    path("palika/list", views.PalikaListView.as_view(), name="palika_list"),
    path("wards/list", views.WardListView.as_view(), name="wards_list"),
]
