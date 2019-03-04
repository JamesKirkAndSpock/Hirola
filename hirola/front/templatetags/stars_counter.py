from django import template
from ..models import PhoneList

register = template.Library()


@register.filter
def checked_star_range(value):
    return range(int(value))


@register.filter
def unchecked_star_range(value):
    value = 5 - int(value)
    return range(value)


@register.filter
def round_off(value):
    return round(value)


@register.filter
def integize(value):
    return range(value-1)
