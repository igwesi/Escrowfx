from django.db import models
import uuid
from apps.accounts.models import User


class Chat(models.Model):
	chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
	read = models.BooleanField(default=False)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.chat_id + " - " + self.user1 + " - " + self.user2


class Message(models.Model):
	message_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	msg = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message_id + "-" + str(self.timestamp)
