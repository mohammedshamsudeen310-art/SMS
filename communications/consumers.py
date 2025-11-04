import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"conversation_{self.conversation_id}"

        allowed = await self.user_is_participant(user.id, self.conversation_id)
        if not allowed:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content):
        msg_type = content.get("type")

        if msg_type == "message.send":
            text = content.get("text", "").strip()
            if not text:
                return

            message = await self.create_message(self.conversation_id, self.scope["user"].id, text)

            payload = {
                "type": "message.broadcast",
                "message": {
                    "id": message.id,
                    "content": message.content,
                    "sender_id": message.sender_id,
                    "sender_username": message.sender.get_full_name() or message.sender.username,
                    "created_at": message.created_at.isoformat(),
                },
            }

            # ✅ Proper type name (underscore, not dot)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "broadcast_message", "payload": payload}
            )

        elif msg_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "user_typing", "user_id": self.scope["user"].id}
            )

    async def broadcast_message(self, event):
        payload = event.get("payload", {})
        if payload:
            await self.send_json(payload)

    async def user_typing(self, event):
        await self.send_json({"type": "typing", "user_id": event["user_id"]})

    @database_sync_to_async
    def user_is_participant(self, user_id, conversation_id):
        from .models import Conversation
        try:
            convo = Conversation.objects.get(pk=conversation_id)
            return convo.participants.filter(pk=user_id).exists()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, conversation_id, sender_id, text):
        convo = Conversation.objects.get(pk=conversation_id)
        sender = User.objects.get(pk=sender_id)
        msg = Message.objects.create(conversation=convo, sender=sender, content=text)
        convo.updated_at = msg.created_at
        convo.save(update_fields=["updated_at"])
        return msg
