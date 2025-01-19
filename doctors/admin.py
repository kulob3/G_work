from django.contrib import admin
from doctors.models import Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality', 'bio', 'photo')
    list_filter = ('name', 'speciality')
    search_fields = ('name', 'speciality')
