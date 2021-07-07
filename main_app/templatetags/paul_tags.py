from django import template
from django.utils.timezone import make_aware
from datetime import datetime

register = template.Library()


@register.filter
def timestamp_from_filter(value: int):
    return make_aware(datetime.fromtimestamp(value))
