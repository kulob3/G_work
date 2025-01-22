from django.urls import path
from django.views.decorators.cache import cache_page
from appointment.apps import AppointmentConfig
from appointment.views import AppointmentCreateView, AppointmentListView, AppointmentDetailView, AppointmentUpdateView, \
    AppointmentDeleteView

app_name = AppointmentConfig.name

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('', cache_page(60)(AppointmentListView.as_view()), name='appointment_list'),
    path('view/<int:pk>/', cache_page(60)(AppointmentDetailView.as_view()), name='appointment_view'),
    path('edit/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete')
]
