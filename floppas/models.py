from django.db import models

class Chat(models.Model):
    user_one = models.ForeignKey(
        'jwt_auth.User',
        related_name='active_chats',
        on_delete=models.CASCADE
    )
    user_two = models.IntegerField()

    def __str__(self):
        return f'User 1: {self.user_id} - User 2: {self.matched_user}'


class Message(models.Model):
    text = models.CharField(max_length= 1000)
    parent_chat = models.ForeignKey(
        Chat,
        related_name='messages_in_chat',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        'jwt_auth.User',
        related_name='sent_messages',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.id} - {self.created_at}'