from django.contrib import admin

from .models import Message, Room, RoomsUsers

admin.site.register(Room)
admin.site.register(RoomsUsers)
admin.site.register(Message)
