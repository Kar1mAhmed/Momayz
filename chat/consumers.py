from channels.generic.websocket import WebsocketConsumer

import json

from .models import Message
from .serializers import MessageSerializer
from .helpers import get_user_from_token, send_message_to_admin

from users.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.user = get_user_from_token(self.scope["url_route"]["kwargs"]["token"])
        
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = User.objects.get(pk=user_id)
        self.room_name = user_id
        
        # # Reject the request if user isn't admin and trying to connect to another user socket
        # if str(self.user.pk) != str(self.room_name) \
        # and not self.user.is_staff \
        # and not self.user.is_superuser:
        #     self.close()
        
        self.room_group_name = f"chat_{self.room_name}"

        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.save_message(text_data_json)
        if not message:
            return 
        self.send(text_data=json.dumps({"message": message}))
        # send the message to admin socket
        send_message_to_admin(message)
        
    
    def save_message(self, text_data_json):
        text = text_data_json.get('text')
        image = text_data_json.get('image')
        voice = text_data_json.get('voice')
        sent_by_admin = True if self.user.is_staff or self.user.is_superuser else False
        
        if not text and not voice and not image:
            return False
        
        message = Message.objects.create(text=text, image=image, voice=voice,
                                            sent_by_admin=sent_by_admin, user=self.user)
        
        return MessageSerializer(message).data
    


class AdminChatConsumer(WebsocketConsumer):
    def connect(self):

        # self.user = get_user_from_token(self.scope["url_route"]["kwargs"]["token"])
        self.room_name = 'admin'
        
        # # Reject the request if user not admin
        # if not self.user.is_superuser and not self.user.is_staff:
        #     self.close()
        
        self.room_group_name = f"chat_{self.room_name}"

        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass
    
    def forward_to_all(self, message):
        self.send(text_data=json.dumps({
            'message': message
        }))