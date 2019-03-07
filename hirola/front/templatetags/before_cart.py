"""
Contains functions for processing information to be displayed
on the cart page.
"""
from django import template
from front.models import PhoneList

register = template.Library()


@register.filter
def features(p_k):
    """Fetch phone information."""
    phone = PhoneList.objects.filter(pk=p_k).first()
    infos = phone.phone_information.all()
    return infos
