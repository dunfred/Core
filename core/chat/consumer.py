import json
from chat.models import Profile, ChatGroup
from chat.serializers import UserSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async  def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )
        await self.accept()

        user = self.scope ['user']
        if user.is_authenticated:
            print(user, "Is authenticated")
            await self.update_user_status(user, True)
        await self.send_status(True)
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        user = self.scope['user']
        if user.is_authenticated:
            await self.update_user_status(user, False)
            await self.send_status(False)
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        responce = text_data_json['message']
        message = responce['text']
        username = responce['username']

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username':username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message':message,
            "event": "Message",
            'username':username,
            }))

    async def send_status (self, is_connected):
        users_count = await self.get_active_users_count()
        user = self.scope['user']


        await self.channel_layer.group_send(self.room_group_name,
            {
                "type": "user_update",
                "event": "Change Status",
                "users_count": users_count,
                "last_joined": user.username.title(),
                "is_connected": is_connected,
            }
        )

    async def user_update(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_active_users_count(self):
        group = ChatGroup.objects.get(id=int(self.room_name))
        return len(User.objects.filter(groups__id=group.id).filter(profile__status=True))

    # @sync_to_async
    # def get_active_users_list(self):
    #     group = ChatGroup.objects.get(id=int(self.room_name))
    #     active_user_list = User.objects.filter(groups__id=group.id).filter(profile__status=True)
    #     serializer_class = UserSerializer(active_user_list, many=True)
    #     return serializer_class.data

    @database_sync_to_async
    def update_user_status (self, user, status):
        return Profile.objects.filter(user_id = user.pk).update(status = status)

