import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from front.models import LandingPageImage
from hirola.settings.base import BASE_DIR



class LandingPageImageModelsTestCase(TestCase):
    def setUp(self):
        LandingPageImage.objects.create(pk=1)
        LandingPageImage.objects.create(phone_name="Phone1", 
            phone_tag="Phone1_Tag", pk=2,
            )
        LandingPageImage.objects.create(phone_name="Phone2", 
            phone_tag="Phone2_Tag", pk=3,
            )
        pass

    def test_that_default_values_are_picked(self):
        """
        Test that a landing page image is created with default values
        """
        get_object = LandingPageImage.objects.get(pk=1)
        self.assertEqual(get_object.carousel_color, 'red')
        self.assertEqual(get_object.text_color, 'white')
        self.assertEqual(get_object.phone_name, '')
        self.assertEqual(get_object.phone_tag, '')

    def test_deletion(self):
        """
        Test that a landing page image can be deleted
        """
        self.assertEqual(len(LandingPageImage.objects.all()), 3)
        get_object = LandingPageImage.objects.get(phone_name="Phone1")
        get_object.delete()
        self.assertEqual(len(LandingPageImage.objects.all()), 2)

    def test_edition(self):
        get_object = LandingPageImage.objects.get(pk=3)
        self.assertEqual(get_object.phone_name, "Phone2")
        self.assertEqual(get_object.phone_tag, "Phone2_Tag")
        get_object.phone_name="Phone2_Prime"
        get_object.phone_tag="Phone2_Tag_Prime"
        get_object.save()
        get_edited_object = LandingPageImage.objects.get(pk=3)
        self.assertNotEqual(get_edited_object.phone_name, "Phone2")
        self.assertNotEqual(get_edited_object.phone_tag, "Phone2_Tag")
        self.assertEqual(get_edited_object.phone_name, "Phone2_Prime")
        self.assertEqual(get_edited_object.phone_tag, "Phone2_Tag_Prime")


class LandingPageImagsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='test',
        )
        self.client.force_login(user)
        self.add_url = "/admin/front/landingpageimage/add/"

    def test_creation_of_entry(self):
        '''
        Test that an image is created and added to the database.
        '''
        image_path = BASE_DIR + '/media/test_image_1.jpeg'
        mock_image = SimpleUploadedFile(name='test_image_1.jpeg',
                                        content=open(image_path, 'rb').read(),
                                        content_type='image/jpeg'
                                        )
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": "test_phone_name1", "phone_tag": "test_phone_tag1",
                "text_color": "white"
            }
        response = self.client.post(self.add_url, form)
        self.assertRedirects(response, '/admin/front/landingpageimage/', 302)
        get_images = LandingPageImage.objects.all()
        self.assertEqual(len(get_images), 1)
        get_image = LandingPageImage.objects.get(pk=1)
        self.assertEqual(get_image.phone_name, 'test_phone_name1')
        self.assertEqual(get_image.phone_tag, 'test_phone_tag1')

    def add_image_before_edit(self):
        image_path = BASE_DIR + '/media/test_image_2.jpeg'
        mock_image_2 = SimpleUploadedFile(name='test_image_2.jpeg',
                                content=open(image_path, 'rb').read(),
                                content_type='image/jpeg'
                                )
        form = {"photo": mock_image_2, "carousel_color": "red",
                "phone_name": "test_phone_name2", "phone_tag": "test_phone_tag2",
                "text_color": "white"
            }
        self.client.post(self.add_url, form)

    def test_edition_of_entry(self):
        '''
        Test that all fields for a created image are editable.
        '''
        self.add_image_before_edit()
        image_path = BASE_DIR + '/media/test_image_2.jpeg'
        get_image = LandingPageImage.objects.get(pk=2)
        self.assertEqual(get_image.phone_name, 'test_phone_name2')
        self.assertEqual(get_image.phone_tag, 'test_phone_tag2')
        self.assertEqual(get_image.carousel_color, 'red')
        self.assertEqual(get_image.text_color, 'white')
        edit_url = "/admin/front/landingpageimage/2/change/"
        mock_image_3 = SimpleUploadedFile(name='test_image_3.jpeg',
                        content=open(image_path, 'rb').read(),
                        content_type='image/jpeg'
                        )
        form = {"photo": mock_image_3, "carousel_color": "green",
                "phone_name": "edited_phone_name2", "phone_tag": "edited_test_phone_tag2",
                "text_color": "black"
            }
        response2 = self.client.post(edit_url, form)
        get_edited_image = LandingPageImage.objects.get(pk=2)
        self.assertEqual(get_edited_image.phone_name, 'edited_phone_name2')
        self.assertEqual(get_edited_image.phone_tag, 'edited_test_phone_tag2')
        self.assertEqual(get_edited_image.carousel_color, 'green')
        self.assertEqual(get_edited_image.text_color, 'black')
        self.assertRedirects(response2, '/admin/front/landingpageimage/', 302)

    def test_tag_name_limits(self):
        '''
        Test that the phone name cannot have more that 30 characters
        Test that the phone tag cannot have more than 60 characters
        ''' 
        image_path = BASE_DIR + '/media/test_image_1.jpeg'
        mock_image = SimpleUploadedFile(name='test_image_1.jpeg',
                                content=open(image_path, 'rb').read(),
                                content_type='image/jpeg'
                                )
        long_phone_name = "a long phone name for creation of an entry of an image"
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": long_phone_name, "phone_tag": "test_phone_tag2",
                "text_color": "white"
            }
        response = self.client.post(self.add_url, form)
        self.assertIn(b"Ensure this value has at most 20 characters (it has 54)", response.content)
        self.assertEqual(response.status_code, 200)
        long_phone_tag = "a long phone tag for creation of an entry of an image"
        long_phone_tag+="with more that 60 characters"
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": "test_name", "phone_tag": long_phone_tag,
                "text_color": "white"
            }
        response2 = self.client.post(self.add_url, form)
        self.assertIn(b"Ensure this value has at most 30 characters (it has 81)", response2.content)
        self.assertEqual(response2.status_code, 200)

    def test_image_size_check(self):
        '''
        Test that an image of width pixel lower than 1280 and height pixel
        lower than 700 cannot be added.
        '''
        image_path = BASE_DIR + '/media/test_image_4.jpeg'
        mock_image = SimpleUploadedFile(name='test_image_4.jpeg',
                    content=open(image_path, 'rb').read(),
                    content_type='image/jpeg'
        )
        form = {"photo": mock_image, "carousel_color": "red",
            "phone_name": "test_phone_4", "phone_tag": "test_phone_tag4",
            "text_color": "white"
        }
        response = self.client.post(self.add_url, form)
        error_message="The dimensions of your image are 225 pixels (width) by"
        error_message+=" 225 pixels (height).\nThe landing page has to have a "
        error_message+="width of 1280 pixels or more and a height of 700 pixels"
        error_message+=" or more for clear images"
        self.assertIn(str.encode(error_message), response.content)
        self.assertEqual(response.status_code, 200)
        
            
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
