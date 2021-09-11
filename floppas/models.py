from django.db import models
from django.db.models.deletion import CASCADE

class Chat(models.Model):
    matched_users = models.ManyToManyField(
        'jwt_auth.User',
        related_name='active_chats',
        blank=True
    )

    def __str__(self):
        return f'Chat {self.id}: {self.matched_users}'


class Message(models.Model):
    text = models.CharField(max_length= 1000)
    parent_chat = models.ForeignKey(
        Chat,
        related_name='messages_in_chat',
        on_delete=CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        'jwt_auth.User',
        related_name='sent_messages',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id} - {self.created_at}'
