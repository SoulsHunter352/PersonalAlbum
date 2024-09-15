import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ProfileFriendRequestNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Метод для подключения к сокету и добавлению в группу
        :return:
        """
        self.user = self.scope['user']  # Получаем пользователя
        self.group_name = f"{self.user.username}_friend_req"  # Записываем имя группы
        await self.channel_layer.group_add(self.group_name, self.channel_name)  # Подключаемся к группе

    async def disconnect(self, code):
        """
        Метод для отключения от сокета и группы
        :param code:
        :return:
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_group_notification(self, event):
        """
        Метод для отправки уведомления пользователю
        :param event:
        :return:
        """
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
                'status': message,
                'sender': sender
            }))
