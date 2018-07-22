from front.base_test import *


class AdminPage(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_superuser(
            username='test',
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
