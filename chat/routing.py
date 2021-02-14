from django.urls import re_path
from . import consumer


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatRoomConsumer), #.as_asgi()
    # re_path(r'ws/active/(?P<room_name>\w+)/$', consumer.ActiveUsersConsumer), #.as_asgi()

]
