from django.urls import path

from .views import ChatAPIView, MessageAPIView, ChatByIDView, GetOrCreateChat

app_name = 'chat'

urlpatterns = [
    path('', ChatAPIView.as_view(),
         name='chats'),
    path('<uuid:chat_id>/', ChatByIDView.as_view(),
         name='chat_detail'),
    path('message/', MessageAPIView.as_view(), name='message'),
    path('get-or-create-chat/', GetOrCreateChat.as_view(), name='get_or_create_chat'),

]
