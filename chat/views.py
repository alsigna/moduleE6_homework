from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import BooleanField, Case, Count, Exists, IntegerField, OuterRef, Subquery, Value, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .forms import MessageForm
from .models import Room


class RoomList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = User.objects.filter(pk=request.user.pk).first()
        else:
            user = None

        rooms = Room.objects.all()
        if user is not None:
            rooms = rooms.annotate(
                user_in_room=Count(
                    Subquery(User.objects.filter(rooms__id__contains=OuterRef("id"), id=user.id).values("id"))
                )
            )
        else:
            rooms = rooms.annotate(
                in_group=Value(0),
            )

        return render(
            request=request,
            template_name="chat/room_list.html",
            context={
                "rooms": rooms,
            },
            status=200,
        )

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(pk=request.user.pk).first()
        else:
            return redirect(request.get_full_path())

        if "_join" in request.POST:
            pk = request.POST.get("_join")
            if pk:
                room: Room = Room.objects.filter(pk=int(pk)).first()
                if room and user not in room.users.all():
                    room.users.add(user)
        elif "_leave" in request.POST:
            pk = request.POST.get("_leave")
            if pk:
                room: Room = Room.objects.filter(pk=int(pk)).first()
                if room and user in room.users.all():
                    room.users.remove(user)
        return redirect(request.get_full_path())


class RoomDetails(LoginRequiredMixin, View):
    def get(self, request, room_id):
        user = User.objects.filter(pk=request.user.pk).first()
        room = Room.objects.filter(id=room_id).first()
        return render(
            request=request,
            template_name="chat/room_details.html",
            context={
                "room": room,
                "user_in_room": user in room.users.all(),
                "msg_form": MessageForm,
            },
            status=200,
        )

    # def post(self, request, room_id):
    #     msg_form = MessageForm(request.POST)
    #     user = User.objects.filter(pk=request.user.pk).first()
    #     if msg_form.is_valid():
    #         msg = msg_form.save(commit=False)
    #         msg.author = user
    #         msg.room = Room.objects.filter(id=room_id).first()
    #         msg.save()

    #         channel_layer = get_channel_layer()
    #         async_to_sync(channel_layer.group_send)(
    #             f"room_{room_id}",
    #             {
    #                 "type": "send_message",
    #                 "room_id": room_id,
    #                 "text": msg.text,
    #                 "user": user.username,
    #             },
    #         )

    #     return redirect(request.get_full_path())
