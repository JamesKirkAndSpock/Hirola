"""
Deactivate the cancel order functionality after two days.
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from front.models import CancelledOrder


class Command(BaseCommand):
    """
    Handles the deactivation of the cancel order functionality
    """
    help = (
        'Checks if an order has been in processing for more than two days'
        'if that is the case, it flags the order as uncancellabe'
        'so that the user cannot be able to cancel it after that window')

    def handle(self, *args, **options):
        try:
            CancelledOrder.objects.all().delete()
        except Exception:
            raise CommandError('Error deleting objects from'
                               'Cancelled orders table')
        self.stdout.write(self.style.SUCCESS(
            'Time: {} cancelled orders deleted successfuly'.
            format(timezone.now())))
