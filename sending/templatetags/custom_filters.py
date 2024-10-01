from django import template
from config.settings import PERIOD_CHOICES

register = template.Library()

@register.filter
def get_period_display(period):
    return dict(PERIOD_CHOICES).get(period, period)