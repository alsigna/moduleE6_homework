from chat.models import Room
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RoomSerializer


class RoomApi(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({"rooms": serializer.data})

    def post(self, request):
        room = request.data.get("room")
        serializer = RoomSerializer(data=room)
        if serializer.is_valid(raise_exception=True):
            _ = serializer.save()
        return Response({"success": "Room was created"})

    def delete(self, request):
        room_id = request.data.get("room").get("id")
        if room_id is not None:
            if (room := Room.objects.filter(id=room_id).first()) is not None:
                room.delete()
                return Response("room was deleted")
            else:
                return Response("no room found")
        return Response("specify room id to delete")
