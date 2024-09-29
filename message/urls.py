from django.urls import path

from message.apps import MessageConfig
from message.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MessageConfig.name


urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]


