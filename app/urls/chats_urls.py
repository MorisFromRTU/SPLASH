from django.urls import path
from app.views.chats import chat_detail, get_or_create_chat, delete_message, chats

urlpatterns = [
    path('', chats ,name='chats'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chat_with/<int:user_id>/', get_or_create_chat, name='get_or_create_chat'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
]
