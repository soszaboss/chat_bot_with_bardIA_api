from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Discussion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    message_user = models.TextField(max_length=3000)
    message_ia = models.TextField(max_length=3000)
    discussion = models.ForeignKey(Discussion, related_name='messages', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)