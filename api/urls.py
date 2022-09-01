from django.urls import path

from .views import RoomApi

urlpatterns = [
    path("room/", RoomApi.as_view()),
]
