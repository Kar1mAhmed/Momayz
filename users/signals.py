# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chat.models import Chat

@receiver(post_save, sender=User)
def create_user_chat(sender, instance, created, **kwargs):
    if created:
        Chat.objects.create(user=instance)