# service/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Doctor

@receiver(pre_save, sender=Doctor)
def populate_doctor_names(sender, instance, **kwargs):
    if instance.email:
        instance.first_name = instance.email.first_name
        instance.last_name = instance.email.last_name