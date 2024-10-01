from django.urls import path

from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]