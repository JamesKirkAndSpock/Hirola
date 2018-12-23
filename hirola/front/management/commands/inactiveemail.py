from django.core.management.base import BaseCommand, CommandError
from front.models import User, InactiveUser
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = ('Checks if a user has not activated his email for {} minutes and moves them to the'
            'Inactive Users table.'.format(settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME)
            )

    def handle(self, *args, **options):
        users = User.objects.exclude(is_active=True)
        for user in users:
            check_time = user.date_joined + timedelta(minutes=settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME)
            if timezone.now() > check_time:
                InactiveUser.objects.create(
                    email=user.email, first_name=user.first_name, last_name=user.last_name,
                    date_joined=user.date_joined, country_code=user.country_code,
                    phone_number=user.phone_number, photo=user.photo, change_email=user.change_email,
                    change_email_tracker=user.change_email_tracker, former_email=user.former_email,
                    password=user.password
                    )
                user.delete()
            print("Finished cleaning up inactive users")
