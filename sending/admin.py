from django.contrib import admin

from sending.models import Sending, SendAttempt


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'period', 'status', 'message', 'number_of_parcels')
    list_filter = ('name', 'status',)
    search_fields = ('datetime', 'period', 'status')

@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'status', 'response', 'sending', 'story_attempt')
    list_filter = ('status',)


