from django import template
from ..models import Services

register = template.Library()


@register.filter
def get_services(pk):
    return Services.objects.filter(service_man=pk)
