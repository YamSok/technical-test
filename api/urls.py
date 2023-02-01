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
    path("", MountainPeakList.as_view(), name="list"),
    path("add/", MountainPeakCreate.as_view(), name="add"),
    path("add-many/", CreateMultiplePeaksView.as_view(), name="add-many"),
    path("<int:pk>/", MountainPeakDetail.as_view(), name="detail"),
    path("search/", MountainPeakSearchWithinZone.as_view(), name="search"),
    path("map", map_view, name="map"),

]
