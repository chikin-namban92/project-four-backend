from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    interests = models.CharField(max_length=300, blank=True)
    catnip = models.BooleanField(blank=True, null=True)
    liked_users = models.ManyToManyField(
        'jwt_auth.User',
        related_name='liked_by',
        blank=True
        )

    def __str__(self):
        return f'Username: {self.username}, User ID: {self.id}'
