from front.base_test import *
from django.core import management
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class UserTest(BaseTestCase):

    def setUp(self):
        super(UserTest, self).setUp()

    def test_cron_change_email_delete(self):
        '''
        Test that if you have users with is_active set to False and that they have joined a period
        longer than settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME.
            - That they no longer exist on the Users table
            - That they exist on the InactiveUsers table
        '''
        minutes = settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME + 1
        User.objects.create(email="sivanna@gmail.com", first_name="Sivanna", last_name="Turimo",
                            is_staff=False, is_active=False, change_email="turimo@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            date_joined=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        User.objects.create(email="tripona@gmail.com", first_name="Tripona", last_name="Tirachi",
                            is_staff=False, is_active=False, change_email="tirachi@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            date_joined=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        self.assertTrue(User.objects.filter(first_name="Sivanna").first())
        self.assertTrue(User.objects.filter(first_name="Tripona").first())
        management.call_command('inactiveuser')
        self.assertFalse(User.objects.filter(first_name="Sivanna").first())
        self.assertFalse(User.objects.filter(first_name="Tripona").first())
        self.assertTrue(InactiveUser.objects.filter(first_name="Sivanna").first())
        self.assertTrue(InactiveUser.objects.filter(first_name="Tripona").first())

    def test_cron_change_email_non_delete(self):
        '''
        Test that if you have users with is_active set to True and that they have joined a period
        longer than settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME.
            - That they remain on the Users table
        '''
        minutes = settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME + 1
        User.objects.create(email="sivanna@gmail.com", first_name="Sivanna", last_name="Turimo",
                            is_staff=False, is_active=True, change_email="turimo@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            date_joined=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        User.objects.create(email="tripona@gmail.com", first_name="Tripona", last_name="Tirachi",
                            is_staff=False, is_active=True, change_email="tirachi@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            date_joined=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        self.assertTrue(User.objects.filter(first_name="Sivanna").first())
        self.assertTrue(User.objects.filter(first_name="Tripona").first())
        management.call_command('inactiveuser')
        self.assertTrue(User.objects.filter(first_name="Sivanna").first())
        self.assertTrue(User.objects.filter(first_name="Tripona").first())
        self.assertFalse(InactiveUser.objects.filter(first_name="Sivanna").first())
        self.assertFalse(InactiveUser.objects.filter(first_name="Tripona").first())

    def test_help_message_contains_the_time(self):
        '''
        Test that when you run the help command on the command inactiveuser
            - That you get the minutes that were set for that command.
        '''
        command_class = management.load_command_class('front', 'inactiveuser')
        self.assertIn('for {} minutes'.format(settings.INACTIVE_EMAIL_EXPIRY_MINUTES_TIME),
                      command_class.help)
