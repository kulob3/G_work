from django.urls import path

from sending.apps import SendingConfig
from sending.views import SendingListView, SendingDetailView

app_name = SendingConfig.name


urlpatterns = [
    path('', SendingListView.as_view(), name='sending_list'),
    path('<int:pk>/', SendingDetailView.as_view(), name='sending_view'),
]