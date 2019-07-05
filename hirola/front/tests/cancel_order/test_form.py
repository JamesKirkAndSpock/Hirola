from front.forms.user_forms import OrderCancellationForm
from front.base_test import BaseTestCase
from django.test import RequestFactory
from front.models import User
from django.core import mail
from django.conf import settings


class OrderCancellationFormTestCase(BaseTestCase):
    """
    Tests that the order cancellation form behaves as expected.
    """

    def setUp(self):
        """
        Initialize environment.
        """
        self.request = RequestFactory()
        super(OrderCancellationFormTestCase, self).setUp()

    def test_successful_validation_of_user_comment(self):
        """
        Test user comment is validated before sending email
        """
        data = {'other_reason': 'I dont like the color.'}
        request = self.request.post('/submit_reason', data)
        form = OrderCancellationForm(request.POST)
        self.assertTrue(form.is_valid())
        data = {'other_reason': '$$$$$%%%%%%%%%%%%%%'}
        request = self.request.post('/submit_reason', data)
        form = OrderCancellationForm(request.POST)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['other_reason'][0], 'Please enter a valid reason')

    def test_send_email(self):
        """
        Test form can send email.
        """
        data = {'other_reason': 'I dont like the color.'}
        request = self.request.post('/submit_reason', data)
        form = OrderCancellationForm(request.POST)
        self.assertTrue(form.is_valid())
        User.objects.create_user(
            email="sivanna@gmail.com", password="secret")
        user = User.objects.get(email="sivanna@gmail.com")
        request.user = user
        form.send_email(request)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.EMAIL_HOST_USER])
        subject = "Reason for Cancelling Order"
        self.assertEqual(mail.outbox[0].subject, subject)
        body = data['other_reason']
        body += '\n'
        body += 'From ' + user.email
        self.assertEqual(mail.outbox[0].body, body)
