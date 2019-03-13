"""
Contains functions for processing information to be displayed
on the cart page.
"""
from django import template
from front.models import PhoneModelList

register = template.Library()


@register.filter
def features(p_k):
    """Fetch phone information."""
    phone = PhoneModelList.objects.filter(pk=p_k).first()
    features = phone.phone_features.all()
    return features
