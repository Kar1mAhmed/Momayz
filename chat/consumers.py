import base64
import json
import json
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.get_user(self.scope.get("headers"))
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        
        # Reject the request if user is not staff and trying to connect to another user socket
        if self.user.pk != self.room_name and not self.user.is_staff:
            self.close()
        
        self.room_group_name = f"chat_{self.room_name}"

        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
        
        
    
    def get_user_from_token(self, token):
        try:
            payload = json.loads(base64.b64decode(token.split('.')[1] + '==').decode('utf-8'))
            user_id = payload.get('user_id')
            return get_user_model().objects.get(username=user_id)
        except (Token.DoesNotExist, User.DoesNotExist, KeyError, json.JSONDecodeError):
            return None

    def get_token_from_headers(self, headers):
        # Search for the "authorization" header within the list of headers
        for key, value in headers:
            if key == b'authorization':
                return value.decode('utf-8')
    
    
    def get_user(self, headers):
        authorization_header = self.get_token_from_headers(headers)
        
        if authorization_header:
            token = authorization_header  # The token is the authorization header
            user = self.get_user_from_token(token)
            if user:
                self.user = user