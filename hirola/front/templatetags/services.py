"""
Contains functions for processing information to be displayed
on the network and repair page.
"""
from django import template
from ..models import Service

register = template.Library()


@register.filter
def get_services(p_k):
    """Get services for a particular service person."""
    return Service.objects.filter(service_man=p_k)


@register.filter
def format_phone_number(phone_number, country_code):
    """Format phone number to a human readable format."""
    phone_number = str(phone_number)
    new_phone_number = phone_number[:3] + ' ' + phone_number[3:]
    formated_number = '+' + str(country_code) + ' ' + str(new_phone_number)
    return formated_number
