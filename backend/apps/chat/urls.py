from django.urls import path

from .views import ChatAPIView, MessageAPIView, ChatByIDView

app_name = 'chat'

urlpatterns = [
    path('', ChatAPIView.as_view(),
         name='chats'),
    path('<uuid:chat_id>/', ChatByIDView.as_view(),
         name='chat_detail'),
    path('message/', MessageAPIView.as_view(), name='message'),
]
