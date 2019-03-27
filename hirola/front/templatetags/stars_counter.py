"""
Contains functionality to process user start ratings.
"""
from django import template

register = template.Library()


@register.filter
def checked_star_range(value):
    """
    Check the range of a checked star.

    Parameters:
        value(int): Value to check the range

    Returns:
        range(object): Contains a sequence of integer from 0
        to the value provided
    """
    return range(int(value))


@register.filter
def unchecked_star_range(value):
    """
    Check the range of an unchecked star.

    Parameters:
        value(int): Value to check the range

    Returns:
        range(object): Contains a sequence of integer from 0
        to the value provided
    """
    value = 5 - int(value)
    return range(value)


@register.filter
def round_off(value):
    """
    Round off value to the nearest whole number.

    Returns:
        round(float): Rounded value
    """
    return round(value)


@register.filter
def integize(value):
    return range(value)
