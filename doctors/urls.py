from django.urls import path
from doctors.apps import DoctorsConfig
from doctors.views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView

app_name = DoctorsConfig.name


urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor_list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor_view'),
    path('create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('edit/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_edit'),
    path('delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
]