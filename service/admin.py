from django.contrib import admin
from service.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'duration')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')