from django import template

register = template.Library()

@register.filter
def checked_star_range(value):
    return range(value)


@register.filter
def unchecked_star_range(value):
    value = 5 - value
    return range(value)