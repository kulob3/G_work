from django.contrib import admin

from sending.models import Sending, Client, Message, SendAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment')
    search_fields = ('name',)

@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'period', 'status', 'message', 'number_of_parcels')
    list_filter = ('name', 'status',)
    search_fields = ('datetime', 'period', 'status')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body')
    search_fields = ('topic',)

@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'status', 'response', 'sending', 'story_attempt')
    list_filter = ('status',)


