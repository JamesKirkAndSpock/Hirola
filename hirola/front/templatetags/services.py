from django import template
from ..models import Service

register = template.Library()


@register.filter
def get_services(pk):
    return Service.objects.filter(service_man=pk)
