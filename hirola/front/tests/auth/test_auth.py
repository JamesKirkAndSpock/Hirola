from front.base_test import BaseTestCase
from django.test import RequestFactory
from front.forms.user_forms import UserCreationForm, loader, get_current_site, urlsafe_base64_encode, force_bytes, account_activation_token, resend_email
from front.models import User, CountryCode
from django.core import mail
from django.conf import settings
import os


class SignupTestCase(BaseTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        super(SignupTestCase, self).setUp()

    def test_send_email(self):
        '''
        Test that the send_email method when given data to send:
            - That it send the data it is expected to send to the recepient.
        Test that when you click the activation link sent once and twice:
            - That on the first click it redirects you to a login page.
            - That on the second click it informs you that the activation link is invalid
        '''
        country_code_k = CountryCode.objects.get(country="Kenya")
        user_data = {"email": "test_user@gmail.com", "first_name": "Test", "last_name": "User",
                     "country_code": country_code_k.pk, "phone_number": 722000000,
                     "password1": "*&#@&!*($)lp", "password2": "*&#@&!*($)lp"}
        request = self.factory.post('/signup', data=user_data)
        form = UserCreationForm(request.POST)
        self.assertEqual(form.is_valid(), True)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.assertEqual(str(user), "Test User")
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = loader.render_to_string("registration/signup_activation_subject.txt", context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string("registration/signup_activation_email.html", context)
        form.send_email(request, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test_user@gmail.com'])
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].body, body)
        email = loader.render_to_string("test/test_email.html", context)
        response = self.client.get(email, follow=True)
        self.assertRedirects(response, "/login?next=/dashboard", 302)
        response_2 = self.client.get(email, follow=True)
        self.assertContains(response_2, "The activation link is invalid!")
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        '''
        Test that when you provide a uid for a user that exists to the get_user method:
            - That the correct user is returned.
        '''
        country_code_k = CountryCode.objects.get(country="Kenya")
        User.objects.create_user(email="test_user_2@gmail.com", first_name="Test",
                                 last_name="User_2", country_code=country_code_k,
                                 phone_number=72200000)
        user = User.objects.get(email="test_user_2@gmail.com")
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        user_get = UserCreationForm().get_user(uid)
        self.assertEqual(user_get.email, "test_user_2@gmail.com")

    def test_get_user_not_exist(self):
        '''
        Test that when a user is provided that does not exist to teh get_user method:
            - That a None object is returned.
        '''
        uid = urlsafe_base64_encode(force_bytes(1111111)).decode()
        user_get = UserCreationForm().get_user(uid)
        self.assertEqual(user_get, None)

    def test_get_user_wrong_value(self):
        '''
        Test that when you provide the wrong value to the get_user method:
            - That a None object is returned.
        '''
        user_get = UserCreationForm().get_user("example")
        self.assertEqual(user_get, None)

    def test_resend_email(self):
        '''
        Test that the send_email method when given data to send:
            - That it send the data it is expected to send to the recepient.
        # Test that when you click the activation link sent once and twice:
        #     - That on the first click it redirects you to a login page.
        #     - That on the second click it informs you that the activation link is invalid
        '''
        country_code_k = CountryCode.objects.get(country="Kenya")
        user_data = {"email": "test_user@gmail.com", "first_name": "Test", "last_name": "User",
                     "country_code": country_code_k.pk, "phone_number": 722000000,
                     "password1": "*&#@&!*($)lp", "password2": "*&#@&!*($)lp"}
        request = self.factory.post('/signup', data=user_data)
        form = UserCreationForm(request.POST)
        self.assertEqual(form.is_valid(), True)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.assertEqual(str(user), "Test User")
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = loader.render_to_string(
            "registration/signup_activation_subject.txt", context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(
            "registration/signup_activation_email.html", context)
        form.send_email(request, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test_user@gmail.com'])
        resend_email(request, user, user_data['email'])
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ['test_user@gmail.com'])
