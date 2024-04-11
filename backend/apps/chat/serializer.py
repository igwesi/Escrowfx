from rest_framework import serializers
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['chat', 'msg']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user2']


class ChatDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
