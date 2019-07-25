from front.base_test import BaseTestCase, Client
from front.models import User


class CancelOrderReasonTestCase(BaseTestCase):
    """
    Tests the functionality for submitting a cancel request reason
    """

    def setUp(self):
        """
        Initialize testing environment.
        """
        super(CancelOrderReasonTestCase, self).setUp()
        User.objects.create(
            email="urieltimanko@example.com", password="secret")
        self.uriel = Client()
        user = User.objects.get(email="urieltimanko@example.com")
        user.is_active = True
        user.save()
        self.uriel.force_login(user)

    def test_submit_reason_success(self):
        """
        Test user can successfuly submit a reason.
        """
        data = {'other_reason': 'I dont like the color.'}
        response = self.uriel.post('/submit_reason', data, follow=True)
        self.assertRedirects(response, '/', 302)

    def test_submit_form_with_error(self):
        """
        Test application does not allow form with error.
        """
        data = {'other_reason': '$$$$$$$$$$$$'}
        response = self.uriel.post('/submit_reason', data)
        self.assertEqual(response.request['PATH_INFO'], '/submit_reason')
