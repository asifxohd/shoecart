from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
import json
from channels.db import database_sync_to_async
from .models import CustomUser
from chat.models import Thread,ChatMessage


User = get_user_model()

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print("websocket_connect", event)
        user = self.scope['user']
        chat_room = f'user_chat_room_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        send_by_id = received_data.get('send_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        if not msg:
            print("error empty-message")
            return False

        send_by_user = await self.get_user_object(send_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)
        await self.create_chat_message(thread_obj, send_by_user, msg)
        if not send_to_user:
            print("no send_to_user")

        if not send_by_user:
            print("no send_by_user")
            
        if not thread_obj:
            print("no thread object found")

        other_user_chat_room = f'user_chat_room_{send_to_id}'

        self_user = self.scope['user']
        response = {
            'message': msg,
            'send_by': send_by_id
        }

        # await self.channel_layer.group_send(
        #     other_user_chat_room,
        #     {
        #         'type': 'chat_message',
        #         'text': json.dumps(response)
        #     }
        # )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        print("message Received", event)

        
    async def websocket_disconnect(self,event):
        print("disconnected", event)
        
    async def chat_message(self, event):
        print("chat message", event)
        await self.send({
            'type':'websocket.send',
            'text':event['text']
            
        })
        
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = CustomUser.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None 
        return obj 
            

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj


    @database_sync_to_async
    def create_chat_message(self, thread, user,message ):
        ChatMessage.objects.create(thread=thread, user=user, message=message)
    