from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
import json
from channels.db import database_sync_to_async
from .models import CustomUser
from chat.models import Thread,ChatMessage
from django.db.models import Q
from channels.exceptions import StopConsumer


User = get_user_model()

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        """
        Called when a WebSocket connection is established.
        """
        print("websocket_connect", event)

        # Access the user information from the connection's scope
        user = self.scope['user']

        # Create a chat room specific to the user using their ID
        chat_room = f'user_chat_room_{user.id}'
        
        # Set the chat room attribute of the instance
        self.chat_room = chat_room

        # Add the connection's channel (WebSocket connection) to the user's chat room group
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.send({
            'type': 'websocket.accept'
        })


    async def websocket_receive(self, event):
        """
        Called when a WebSocket receives a message.
        """
        # Get the received data from the event
        received_data = event.get('text', '')
        print("Received data:", received_data)

        # Check if the received data is empty or missing 'text' in WebSocket message
        if not received_data:
            print("warning: received empty or missing 'text' in WebSocket message")
            return

        # Try to decode the received data as JSON
        try:
            received_data = json.loads(received_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

        # Extract relevant data from the received JSON
        msg = received_data.get('message')
        send_by_id = received_data.get('send_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')
        print(thread_id)

        # Check for an existing thread or create a new one
        existing_thread = await self.get_existing_thread(send_by_id, send_to_id)
        if existing_thread:
            thread_obj = existing_thread
        elif thread_id:
            thread_obj = await self.get_thread(thread_id)
            if not thread_obj:
                thread_obj = await self.create_thread(send_by_id, send_to_id)
        else:
            thread_obj = await self.create_thread(send_by_id, send_to_id)

        # Check for an empty message
        if not msg:
            print("error empty-message")
            return False

        # Get user objects for the sender and recipient
        send_by_user = await self.get_user_object(send_by_id)
        send_to_user = await self.get_user_object(send_to_id)

        # Create a chat message in the specified thread
        await self.create_chat_message(thread_obj, send_by_user, msg)

        # Print messages if certain objects are not found
        if not send_to_user:
            print("no send_to_user")
        if not send_by_user:
            print("no send_by_user")
        if not thread_obj:
            print("no thread object found")

        # Define the chat room for the recipient
        other_user_chat_room = f'user_chat_room_{send_to_id}'

        # Get the user information from the connection's scope
        self_user = self.scope['user']

        # Prepare a response to send to the user's chat room
        response = {
            'message': msg,
            'send_by': send_by_id
        }

        # Send the response to the user's chat room group
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        # Print a message indicating that a message was received
        print("message Received", event)



        
    async def websocket_disconnect(self, event):
        """
        Called when a WebSocket connection is closed.
        """
        # Access the user information from the connection's scope
        user = self.scope['user']

        # Remove the user from the chat room group
        await self.channel_layer.group_discard(
            f'user_chat_room_{user.id}',
            self.channel_name
        )

        # Print a message indicating disconnection and raise StopConsumer to stop the consumer
        print("Disconnected", event)
        raise StopConsumer()


    async def chat_message(self, event):
        """
        Called when a chat message is received.
        """
        # Print information about the chat message event
        print("chat message", event)

        # Send the received message to the connected client
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })


    @database_sync_to_async
    def get_user_object(self, user_id):
        """
        Retrieve a user object from the database asynchronously.
        """
        # Query the database for a user with the specified ID
        qs = CustomUser.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj


    @database_sync_to_async
    def get_thread(self, thread_id):
        """
        Retrieve a thread object from the database asynchronously.
        """
        # Query the database for a thread with the specified ID
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj


    @database_sync_to_async
    def create_chat_message(self, thread, user, message):
        """
        Create a chat message in the database asynchronously.
        """
        # Print information about the thread, user, and message
        print(thread)
        print(user)
        print(message)

        # Create a new chat message in the database
        ChatMessage.objects.create(thread=thread, user=user, message=message)


    @database_sync_to_async
    def create_thread(self, user1_id, user2_id):
        """
        Create a thread between two users in the database asynchronously.
        """
        # Retrieve user objects for the specified IDs
        user1 = CustomUser.objects.get(id=user1_id)
        user2 = CustomUser.objects.get(id=user2_id)

        # Create a new thread in the database
        thread = Thread.objects.create(first_person=user1, admin=user2)

        return thread


    @database_sync_to_async
    def get_existing_thread(self, user1_id, user2_id):
        """
        Retrieve an existing thread between two users from the database asynchronously.
        """
        # Query the database for a thread between the specified users
        qs = Thread.objects.filter(Q(first_person_id=user1_id, admin_id=user2_id) | Q(first_person_id=user2_id, admin_id=user1_id))
        if qs.exists():
            # Return the first matching thread
            return qs.first()
        return None
