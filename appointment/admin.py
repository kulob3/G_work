from django.contrib import admin

from appointment.models import Appointment


@admin.register(Appointment)
class Appointment(admin.ModelAdmin):
    list_display = ('name', 'client', 'service', 'appointment_number_int', 'date', 'time', 'price', 'status', 'comment', 'result')
