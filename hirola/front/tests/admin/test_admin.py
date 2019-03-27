
"""Contains tests for admin functionality."""
from front.base_test import User, Client, TestCase


class AdminPage(TestCase):
    """Tests the admin page."""

    def setUp(self):
        """
        Set up test pre-conditions.
        """
        self.client = Client()
        user = User.objects.create_superuser(
            email='test@example.com',
            password='test',
        )
        self.client.force_login(user)

    def test_admin_title_exists(self):
        '''
        Test that the Title on the admin page is customized to Hirola Admin
        Panel and not Django adminstration.
        '''
        response = self.client.get('/admin/')
        self.assertContains(response, "Hirola Admin Panel")
        self.assertNotContains(response, "Django administration")
