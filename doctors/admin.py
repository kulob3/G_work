from django.contrib import admin
from doctors.models import Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'speciality', 'bio', 'photo')
