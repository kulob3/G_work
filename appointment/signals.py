import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from appointment.models import Appointment

@receiver(post_save, sender=Appointment)
def send_status_change_email(sender, instance, **kwargs):
    if 'status' in instance.get_dirty_fields():
        user_email = instance.client.email.email  # Fetch email from related User model
        send_mail(
            'Изменение статуса приема',
            f'Статус вашего приема изменен на: {instance.get_status_display()}',
            '9272060714@mail.ru',
            [user_email],
            fail_silently=False,
        )