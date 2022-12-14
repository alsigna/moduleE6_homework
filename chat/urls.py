from django.urls import path
from .websocket import ChatConsumer, RoomListConsumer
from django.urls import include, path
from rest_framework import routers

from .views import RoomList, RoomDetails

app_name = "chat"

# router = routers.DefaultRouter()
# router.register(r"heroes", views.HeroViewSet)

urlpatterns = [
    path("", RoomList.as_view(), name="main"),
    path("room/<int:room_id>/", RoomDetails.as_view(), name="room_details"),
    path("api/", include("api.urls")),
    # path("<int:room_id>/leave", LeaveRoom.as_view(), name="leave_room"),
]


websocket_urlpatterns = [
    path("ws/room/<int:room_id>/<str:username>/", ChatConsumer.as_asgi()),
    path("ws/roomlist/<str:username>/", RoomListConsumer.as_asgi()),
]
