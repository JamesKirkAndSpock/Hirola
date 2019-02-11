from front.base_test import BaseTestCase
from django.core import management
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from front.models import (InactiveUser, User)

class UserTest(BaseTestCase):

    def setUp(self):
        super(UserTest, self).setUp()

    def test_cron_inactive_user_delete(self):
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
        sivanna_user = User.objects.get(email="sivanna@gmail.com")
        triponna_user = User.objects.get(email="tripona@gmail.com")
        self.assertTrue(User.objects.filter(first_name="Sivanna").first())
        self.assertTrue(User.objects.filter(first_name="Tripona").first())
        management.call_command('inactiveuser')
        self.assertFalse(User.objects.filter(first_name="Sivanna").first())
        self.assertFalse(User.objects.filter(first_name="Tripona").first())
        self.assertTrue(InactiveUser.objects.filter(first_name="Sivanna").first())
        self.assertTrue(InactiveUser.objects.filter(first_name="Tripona").first())
        inactive_sivanna = InactiveUser.objects.get(first_name="Sivanna")
        inactive_triponna = InactiveUser.objects.get(first_name="Tripona")
        self.assertEqual(inactive_sivanna.email, sivanna_user.email)
        self.assertEqual(inactive_sivanna.first_name, sivanna_user.first_name)
        self.assertEqual(inactive_sivanna.last_name, sivanna_user.last_name)
        self.assertEqual(inactive_sivanna.date_joined, sivanna_user.date_joined)
        self.assertEqual(inactive_sivanna.country_code, sivanna_user.country_code)
        self.assertEqual(inactive_sivanna.phone_number, sivanna_user.phone_number)
        self.assertEqual(inactive_sivanna.photo, sivanna_user.photo)
        self.assertEqual(inactive_sivanna.change_email, sivanna_user.change_email)
        self.assertEqual(inactive_sivanna.change_email_tracker, sivanna_user.change_email_tracker)
        self.assertEqual(inactive_sivanna.former_email, sivanna_user.former_email)
        self.assertEqual(inactive_sivanna.password, sivanna_user.password)
        self.assertEqual(inactive_triponna.email, triponna_user.email)
        self.assertEqual(inactive_triponna.first_name, triponna_user.first_name)
        self.assertEqual(inactive_triponna.last_name, triponna_user.last_name)
        self.assertEqual(inactive_triponna.date_joined, triponna_user.date_joined)
        self.assertEqual(inactive_triponna.country_code, triponna_user.country_code)
        self.assertEqual(inactive_triponna.phone_number, triponna_user.phone_number)
        self.assertEqual(inactive_triponna.photo, triponna_user.photo)
        self.assertEqual(inactive_triponna.change_email, triponna_user.change_email)
        self.assertEqual(inactive_triponna.change_email_tracker, triponna_user.change_email_tracker)
        self.assertEqual(inactive_triponna.former_email, triponna_user.former_email)
        self.assertEqual(inactive_triponna.password, triponna_user.password)



    def test_cron_inactive_user_non_delete(self):
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
