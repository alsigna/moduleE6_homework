import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Room, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class RoomListConsumer(AsyncJsonWebsocketConsumer):
    def check_user_in_room(self, room_id):
        user = User.objects.get(username=self.username)
        print(f"{user=}")
        print(f"{room_id=}")
        return user.rooms.filter(id=room_id).exists()

    async def clean_kwargs(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]

    async def connect(self):
        await self.clean_kwargs()
        await self.channel_layer.group_add(
            group="room_list",
            channel=self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            group="room_list",
            channel=self.channel_name,
        )

    async def send_message(self, res):
        print(f"{res=}")
        user_in_room = await database_sync_to_async(self.check_user_in_room)(res.get("room_id"))
        print(f"{user_in_room=}")
        if user_in_room:
            await self.send(text_data=json.dumps(res))


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def check_user_in_room(self):
        user = User.objects.get(username=self.username)
        room = Room.objects.get(id=self.room_id)
        return user in room.users.all()

    def save_new_message(self, text):
        user = User.objects.get(username=self.username)
        room = Room.objects.get(id=self.room_id)
        message = Message.objects.create(author=user, room=room, text=text)

    async def clean_kwargs(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_name = f"room_{self.room_id}"

    async def connect(self):
        await self.clean_kwargs()
        user_in_room = await database_sync_to_async(self.check_user_in_room)()
        if user_in_room:
            await self.channel_layer.group_add(
                group=self.room_name,
                channel=self.channel_name,
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            group=self.room_name,
            channel=self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        username = data.get("username", None)
        text = data.get("text", None)
        await database_sync_to_async(self.save_new_message)(text)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send_message",
                "text": text,
                "room_id": self.room_id,
                "username": username,
            },
        )
        await self.channel_layer.group_send(
            "room_list",
            {
                "type": "send_message",
                "room_id": self.room_id,
            },
        )

    async def send_message(self, res):
        print(f"{res=}")
        await self.send(text_data=json.dumps(res))
