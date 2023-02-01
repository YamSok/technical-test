from django.urls import path

from .views import (
    MountainPeakList,
    MountainPeakDetail,
    MountainPeakCreate,
    CreateMultiplePeaksView,
    MountainPeakSearchWithinZone,
)
from .views import map_view

urlpatterns = [
    path("", MountainPeakList.as_view(), name="item-list"),
    path("add/", MountainPeakCreate.as_view(), name="item-create"),
    path("add-many/", CreateMultiplePeaksView.as_view(), name="item-create-many"),
    path("<int:pk>/", MountainPeakDetail.as_view(), name="item-detail"),
    path("map", map_view, name="map"),
    path("search/", MountainPeakSearchWithinZone.as_view(), name="search"),
]
