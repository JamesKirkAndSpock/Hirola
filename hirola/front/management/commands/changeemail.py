from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from front.models import User
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = ('Sets the change_email field to None for users who have '
            'not edited their emails after'
            ' {} minutes'.format(settings.CHANGE_EMAIL_EXPIRY_MINUTES_TIME)
            )

    def handle(self, *args, **options):
        users = self.get_users()
        try:
            for user in users:
                check_time = user.change_email_tracker + timedelta(
                    minutes=settings.CHANGE_EMAIL_EXPIRY_MINUTES_TIME
                    )
                if timezone.now() > check_time:
                    user.change_email = None
                    user.change_email_tracker = None
                    user.save()
        except Exception:
            raise CommandError("Error resetting the changeemail command")
        self.stdout.write(self.style.SUCCESS(
            'Time: {} changeemail command run successful'.
            format(timezone.now())))

    def get_users(self):
        try:
            return User.objects.exclude(change_email=None)
        except Exception:
            raise CommandError("Error getting users from the application")
