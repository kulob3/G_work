from django.urls import path
from django.views.decorators.cache import cache_page
from appointment.apps import AppointmentConfig
from appointment.views import AppointmentCreateView, AppointmentListView, AppointmentDetailView, AppointmentUpdateView, \
    AppointmentDeleteView, cancel_appointment, confirm_appointment

app_name = AppointmentConfig.name

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('view/<int:pk>/', cache_page(60)(AppointmentDetailView.as_view()), name='appointment_view'),
    path('edit/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_edit'),
    path('delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('cancel/<int:pk>/', cancel_appointment, name='appointment_cancel'),
    path('<int:pk>/confirm/', confirm_appointment, name='appointment_confirm'),
]
