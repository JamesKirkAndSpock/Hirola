from django.core.management.base import BaseCommand, CommandError
from front.models import User
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = ('Sets the change_email field to None for users who have not edited their emails after'
            ' {} minutes'.format(settings.CHANGE_EMAIL_EXPIRY_MINUTES_TIME)
            )

    def handle(self, *args, **options):
        users = User.objects.exclude(change_email=None)
        for user in users:
            check_time = user.change_email_tracker + timedelta(minutes=5)
            if timezone.now() > check_time:
                user.change_email = None
                user.change_email_tracker = None
                user.save()
