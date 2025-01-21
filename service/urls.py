from django.urls import path
from service.apps import ServiceConfig
from service.views import ServiceCreateView, ServiceListView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView

app_name = ServiceConfig.name


urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_view'),
    path('create/', ServiceCreateView.as_view(), name='service_create'),
    path('edit/<int:pk>/', ServiceUpdateView.as_view(), name='service_edit'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),
]