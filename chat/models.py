from django.db import models
from users.models import User

class Chat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                            null=True, related_name='message_sender', unique=True)

class Message(models.Model):
    sent_by_admin = models.BooleanField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    voice = models.URLField(blank=True, null=True)
    duration = models.SmallIntegerField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    
    
    class Meta: 
        ordering = ('time',)
        
    def __str__(self) -> str:
        text = self.text if self.text is not None else "-Link-"
        return f"Conversation({self.conversation.pk})-:{self.sender}--> {text}"