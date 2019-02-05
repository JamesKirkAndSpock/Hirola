from front.base_test import *
from django.core import management
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from front.forms.user_forms import (
    EmailAuthenticationForm, ChangeEmailForm, loader, get_current_site, urlsafe_base64_encode,
    force_bytes, email_activation_token, resend_activation_email)
from django.test import RequestFactory
from django import forms
from django.core import mail


class EmailTest(BaseTestCase):

    def setUp(self):
        super(EmailTest, self).setUp()

    def test_cron_change_email_delete(self):
        '''
        Test that if you have users with change_email set to an email and change_email_tracker to a
        timezone one minute more than the limit, when you run the changeemail command that:
            - their change_email attribute is set to None
            - their change_email_tracker is set to None
        '''
        minutes = settings.CHANGE_EMAIL_EXPIRY_MINUTES_TIME + 1
        User.objects.create(email="sivanna@gmail.com", first_name="Sivanna", last_name="Turimo",
                            is_staff=False, is_active=True, change_email="turimo@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        User.objects.create(email="tripona@gmail.com", first_name="Tripona", last_name="Tirachi",
                            is_staff=False, is_active=True, change_email="tirachi@gmail.com",
                            change_email_tracker=timezone.now()-timedelta(minutes=minutes),
                            phone_number=72200000, )
        sivanna_before = User.objects.get(first_name="Sivanna")
        tripona_before = User.objects.get(first_name="Tripona")
        self.assertTrue(sivanna_before.change_email)
        self.assertTrue(tripona_before.change_email)
        self.assertTrue(sivanna_before.change_email_tracker)
        self.assertTrue(tripona_before.change_email_tracker)
        management.call_command('changeemail')
        sivanna_after = User.objects.get(first_name="Sivanna")
        tripona_after = User.objects.get(first_name="Tripona")
        self.assertFalse(sivanna_after.change_email)
        self.assertFalse(tripona_after.change_email)
        self.assertFalse(sivanna_after.change_email_tracker)
        self.assertFalse(tripona_after.change_email_tracker)

    def test_cron_change_email_non_delete(self):
        '''
        Test that if you have users with change_email set to an email and change_email_tracker to a
        timezone less than the limit, when you run the changeemail command that:
            - their change_email attribute is not set to None
            - their change_email_tracker is not set to None
        '''
        User.objects.create(email="sivanna@gmail.com", first_name="Sivanna", last_name="Turimo",
                            is_staff=False, is_active=True, change_email="turimo@gmail.com",
                            change_email_tracker=timezone.now(),
                            phone_number=72200000, )
        User.objects.create(email="tripona@gmail.com", first_name="Tripona", last_name="Tirachi",
                            is_staff=False, is_active=True, change_email="tirachi@gmail.com",
                            change_email_tracker=timezone.now(),
                            phone_number=72200000, )
        sivanna_before = User.objects.get(first_name="Sivanna")
        tripona_before = User.objects.get(first_name="Tripona")
        self.assertTrue(sivanna_before.change_email)
        self.assertTrue(tripona_before.change_email)
        self.assertTrue(sivanna_before.change_email_tracker)
        self.assertTrue(tripona_before.change_email_tracker)
        management.call_command('changeemail')
        sivanna_after = User.objects.get(first_name="Sivanna")
        tripona_after = User.objects.get(first_name="Tripona")
        self.assertTrue(sivanna_after.change_email)
        self.assertTrue(tripona_after.change_email)
        self.assertTrue(sivanna_after.change_email_tracker)
        self.assertTrue(tripona_after.change_email_tracker)

    def test_help_message_contains_the_time(self):
        '''
        Test that when you run the help command on the command inactiveuser
            - That you get the minutes that were set for that command.
        '''
        command_class = management.load_command_class('front', 'changeemail')
        self.assertIn('after {} minutes'.format(settings.CHANGE_EMAIL_EXPIRY_MINUTES_TIME),
                      command_class.help)

    def test_email_match_check_fail(self):
        '''
        Test that when a user is logging in inorder to be able to edit his email that when enters
        the correct email and password of another user:
            - That a check is made to ensure that an error is raised and the form is considered
            invalid
        '''
        request = RequestFactory()
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        # create another user with some credentials for testing
        User.objects.create_user(email="tripona@gmail.com", password="secret")
        user = User.objects.get(email="sivanna@gmail.com")
        request = request.post("", {'email': 'tripona@gmail.com', 'password': 'secret'})
        request.user = user
        form = EmailAuthenticationForm(request, request.POST)
        self.assertFalse(form.is_valid())
        self.assertIn(form.error_messages['invalid_email'], form.errors['email'])

    def test_email_match_check_pass(self):
        '''
        Test that when a user is logging in inorder to be able to edit his email that when enters
        the correct email and password of his own:
            - That a valid result is returned on the form.
        '''
        request = RequestFactory()
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        user = User.objects.get(email="sivanna@gmail.com")
        request = request.post("", {'email': 'sivanna@gmail.com', 'password': 'secret'})
        request.user = user
        form = EmailAuthenticationForm(request, request.POST)
        self.assertTrue(form.is_valid())

    def test_email_match_check_fail_change_form(self):
        '''
        Test that when you provide the form with a post request with data for the email similar to
        the initial email of the user:
            - That the form is rendered as invalid
            - That an error is raised
        '''
        request = RequestFactory()
        request = request.post("", {'email': 'sivanna@gmail.com', 'password': 'secret'})
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        form = ChangeEmailForm(request.POST, instance=request.user)
        self.assertFalse(form.is_valid())
        self.assertIn(form.error_messages['invalid_email'], form.errors['email'])

    def test_email_match_check_fail_1_change_form(self):
        '''
        Test that when you provide the form with a post request with data for the email different to
        the initial email of the user but non-unique:
            - That the form is rendered as invalid
            - That an error is raised
        '''
        request = RequestFactory()
        request = request.post("", {'email': 'tripona@gmail.com', 'password': 'secret'})
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        User.objects.create_user(email="tripona@gmail.com", password="secret")
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        form = ChangeEmailForm(request.POST, instance=request.user)
        self.assertFalse(form.is_valid())
        error_message = "The email address you entered has already been registered."
        self.assertIn(error_message, form.errors['email'])

    def test_email_match_check_pass_change_form(self):
        '''
        Test that when you provide the form with a post request with data for the email different to
        the initial email of the user and unique:
            - That the form is valid
        '''
        request = RequestFactory()
        request = request.post("", {'email': 'tripona@gmail.com', 'password': 'secret'})
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        form = ChangeEmailForm(request.POST, instance=request.user)
        self.assertTrue(form.is_valid())

    def test_send_email(self):
        '''
        Test that the send_email method when given data to send:
            - That it sends the data it is expected to send to the recepient.
        Test that when you click the activation link sent once and twice:
            - That on the first click it redirects you to a login page.
            - That on the second click it informs you that the activation link is invalid
        '''
        request = RequestFactory()
        request = request.post("", {'email': 'naisomia@gmail.com', 'password': 'secret'})
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        form = ChangeEmailForm(request.POST, instance=request.user)
        self.assertEqual(form.is_valid(), True)
        user.change_email = form.cleaned_data.get('email')
        user.change_email_tracker = timezone.now()
        user.save()
        form.send_email(request, user)
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': email_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = loader.render_to_string("front/change_email_activation_subject.txt", context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string("front/change_email_activation_email.html", context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['naisomia@gmail.com'])
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].body, body)
        email = loader.render_to_string("test/test_change_email.html", context)
        response = self.client.get(email, follow=True)
        self.assertRedirects(response, "/login?next=/dashboard", 302)
        response_2 = self.client.get(email, follow=True)
        self.assertContains(response_2, "The activation link is invalid!")
        self.assertEqual(response.status_code, 200)

    def test_resend_new_email_activation_link(self):
        '''
        Test that the send_email method when given data to send:
            - That it sends the data it is expected to send to the recepient.
        '''
        request = RequestFactory()
        request = request.post("", {
                                    'email': 'naisomia@gmail.com',
                                    'password': 'secret'
                                    })
        User.objects.create_user(email="sivanna@gmail.com", password="secret", )
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        resend_activation_email(request, user, "ndungu@gmail.com")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['ndungu@gmail.com'])

