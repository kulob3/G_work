from django.urls import path

from sending.apps import SendingConfig
from sending.views import SendingListView, SendingDetailView, SendingCreateView, SendingUpdateView, SendingDeleteView, \
    get_mailing_status, home
from . import views
app_name = SendingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('list/', SendingListView.as_view(), name='sending_list'),
    path('<int:pk>/', SendingDetailView.as_view(), name='sending_view'),
    path('create/', SendingCreateView.as_view(), name='sending_create'),
    path('edit/<int:pk>/', SendingUpdateView.as_view(), name='sending_edit'),
    path('delete/<int:pk>/', SendingDeleteView.as_view(), name='sending_delete'),
    path('start_all_mailings/', views.start_all_mailings, name='start_all_mailings'),
    path('stop_all_mailings/', views.stop_all_mailings, name='stop_all_mailings'),
    path('get_mailing_status/', get_mailing_status, name='get_mailing_status'),
]

