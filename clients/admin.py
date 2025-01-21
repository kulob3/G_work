from django.contrib import admin
from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'comment')
    search_fields = ('last_name',)
