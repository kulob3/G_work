from django.core.management.base import BaseCommand
from sending.services import send_mailing

class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **kwargs):
        send_mailing()