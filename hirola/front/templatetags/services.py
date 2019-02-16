from django import template
from ..models import Service

register = template.Library()


@register.filter
def get_services(pk):
    return Service.objects.filter(service_man=pk)


@register.filter
def format_phone_number(phone_number, country_code):
    phone_number = str(phone_number)
    new_phone_number = phone_number[:3] + ' ' + phone_number[3:]
    formated_number = '+' + str(country_code) + ' ' + str(new_phone_number)
    return formated_number
