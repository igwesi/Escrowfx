from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.models import User
from .models import Chat, Message
from .serializer import ChatDetailSerializer, ChatSerializer, CreateMessageSerializer, MessageSerializer


class CustomValidationException(Exception):
    def __init__(self, error, message, status_code=status.HTTP_400_BAD_REQUEST, *args, **kwargs):
        self.error = error,
        self.message = message,
        self.status_code = status_code
        super().__init__(*args, **kwargs)


class ChatAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    serializer_class_detail = ChatDetailSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        chats_1 = Chat.objects.filter(
            user1=user).select_related('user1', 'user2')
        chats_2 = Chat.objects.filter(
            user2=user).select_related('user1', 'user2')
        if not chats_1.exists() and not chats_2.exists():
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": "No chats found.",
                "data": [],
            }, status=status.HTTP_404_NOT_FOUND
            )
        if chats_1.exists():
            chat_data = []
            for chat in chats_1:
                last_message = Message.objects.filter(
                    chat=chat).order_by('-timestamp').first()

                if chat.user_1 == user:
                    other_user_name = chat.user_2.first_name
                else:
                    other_user_name = chat.user_1.first_name

                chat_serializer = self.serializer_class_detail(chat)
                if last_message:
                    message_serializer = MessageSerializer(last_message)
                else:
                    message_serializer = None

                chat_data.append({
                    'chat': chat_serializer.data,
                    'last_message': message_serializer.data if message_serializer else None,
                    'other_user_name': other_user_name,
                })

            return Response({
                "statusCode": status.HTTP_200_OK,
                "message": "Successfully.",
                "data": chat_data,
            }, status=status.HTTP_200_OK)
        else:
            chat_data = []
            for chat in chats_2:
                last_message = Message.objects.filter(
                    chat=chat).order_by('-timestamp').first()

                if chat.user1 == user:
                    other_user_name = chat.user2.first_name
                else:
                    other_user_name = chat.user1.first_name

                chat_serializer = self.serializer_class_detail(chat)

                if last_message:
                    message_serializer = MessageSerializer(last_message)
                else:
                    message_serializer = None

                chat_data.append({
                    'chat': chat_serializer.data,
                    'last_message': message_serializer.data if message_serializer else None,
                    'other_user_name': other_user_name,
                })

            return Response({
                "statusCode": status.HTTP_200_OK,
                "message": "Successfully.",
                "data": chat_data,
            }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user2 = request.data.get("user2")
        try:
            if serializer.is_valid():
                user1 = request.user
                user2 = User.objects.get(id=user2)
                chat = Chat.objects.filter(user1=user1, user_2=user2)
                if chat.exists():
                    raise CustomValidationException(
                        "Chat already exists.", "Chat already exists.")
                chat = Chat.objects.create(
                    user1=user1, user2=user2)
                return Response({
                    "statusCode": status.HTTP_201_CREATED,
                    "message": "Successfully.",
                    "data": ChatDetailSerializer(chat).data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomValidationException(
                    serializer.errors, "Validation error.")
        except CustomValidationException as e:
            return Response({
                "statusCode": e.status_code,
                "message": "Validation error.",
                "error": e.error,
            }, status=e.status_code
            )
        except Exception as e:
            return Response({
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Server error",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChatByIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            chat_id = kwargs.get('chat_id')
            chat = Chat.objects.filter(id=chat_id).select_related(
                'user1', 'user2').first()
            if not chat:
                raise NotFound("Chat not found.")
            serializer = ChatDetailSerializer(chat)
            messages = Message.objects.filter(chat=chat).select_related(
                'chat', 'sender')
            return Response({
                "statusCode": status.HTTP_200_OK,
                "message": "Successfully.",
                "data": {
                            "chat": serializer.data,
                            "messages": MessageSerializer(messages, many=True).data,
                            }
            }, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": "Data error.",
                "error": str(e),
            }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Server error",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            chat_id = kwargs.get('chat_id')
            chat = Chat.objects.filter(id=chat_id).select_related(
                'user1', 'user2').first()
            if not chat:
                raise NotFound("Chat not found.")
            messages = Message.objects.filter(chat=chat).select_related(
                'chat', 'sender')
            if not messages.exists():
                raise NotFound("No messages found for the chat.")
            serializer = MessageSerializer(messages, many=True)
            return Response({
                "statusCode": status.HTTP_200_OK,
                "message": "Successfully.",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({
                "statusCode": status.HTTP_404_NOT_FOUND,
                "message": "Data error.",
                "error": str(e),
            }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Server error",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        serializer = CreateMessageSerializer(data=request.data)
        chat_id = request.data.get("chat")
        try:
            if serializer.is_valid():
                try:
                    chat = Chat.objects.get(id=chat_id)
                except Chat.DoesNotExist:
                    raise CustomValidationException(
                        "Chat not found.", "Chat not found.")
                message = Message.objects.create(
                    chat=chat, sender=request.user, msg=serializer.validated_data.get('message'))
                return Response({
                    "statusCode": status.HTTP_201_CREATED,
                    "message": "Successfully.",
                    "data": MessageSerializer(message).data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomValidationException(
                    serializer.errors, "Validation error.")
        except Exception as e:
            return Response({
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Server error",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
