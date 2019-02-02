from django import template

register = template.Library()

@register.filter
def total_price(value, arg):
    return int(value) * int(arg)

@register.filter
def actualize_quantity(value):
    return int(value) + 1