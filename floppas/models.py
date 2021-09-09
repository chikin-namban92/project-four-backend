from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=500)
    age = models.IntegerField()
    location = models.CharField(max_length=50)
    interests = models.CharField(max_length=300)
    catnip = models.BooleanField()
    liked_users = models.IntegerField(default=None, null=True, blank=True)
    liked_by = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f'Username: {self.username}, User ID: {self.id}'