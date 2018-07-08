from front.base_test import *
from front.errors import *


class LandingPageImagsViewsTestCase(BaseTestCase):
    def setUp(self):
        super(LandingPageImagsViewsTestCase, self).setUp()
        self.add_url = "/admin/front/landingpageimage/add/"

    def test_creation_of_entry(self):
        '''
        Test that an image is created and added to the database.
        Test tha carousel colors appear
        '''
        mock_image = image('test_image_1.jpeg')
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": "test_phone_name1",
                "phone_tag": "test_phone_tag1", "text_color": "white"}
        response = self.elena.post(self.add_url, form)
        self.assertRedirects(response, '/admin/front/landingpageimage/', 302)
        get_images = LandingPageImage.objects.all()
        self.assertEqual(len(get_images), 1)
        get_image = LandingPageImage.objects.get(pk=1)
        self.assertEqual(get_image.phone_name, 'test_phone_name1')
        self.assertEqual(get_image.phone_tag, 'test_phone_tag1')
        response = self.client.get('/')
        self.assertContains(response, "red")
        self.assertContains(response, "white")

    def add_image_before_edit(self):
        mock_image_2 = image('test_image_2.jpeg')
        form = {"photo": mock_image_2, "carousel_color": "red",
                "phone_name": "test_phone_name2",
                "phone_tag": "test_phone_tag2", "text_color": "white"}
        self.elena.post(self.add_url, form)

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
        mock_image = SimpleUploadedFile(name='test_image_3.jpeg',
                                        content=open(image_path, 'rb').read(),
                                        content_type='image/jpeg')
        form = {"photo": mock_image, "carousel_color": "green",
                "phone_name": "edited_phone_name2",
                "phone_tag": "edited_test_phone_tag2", "text_color": "black"}
        response2 = self.elena.post(edit_url, form)
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
        mock_image = image('test_image_1.jpeg')
        long_phone_name = ('a long phone name for creation of an entry of an '
                           'image')
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": long_phone_name, "phone_tag": "test_phone_tag2",
                "text_color": "white"}
        response = self.elena.post(self.add_url, form)
        e_mess_1 = b"Ensure this value has at most 20 characters (it has 54)"
        self.assertIn(e_mess_1, response.content)
        self.assertEqual(response.status_code, 200)
        long_phone_tag = ('a long phone tag for creation of an entry of an '
                          'image with more that 60 characters')
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": "test_name", "phone_tag": long_phone_tag,
                "text_color": "white"}
        response2 = self.elena.post(self.add_url, form)
        e_mess_2 = b"Ensure this value has at most 30 characters (it has 82)"
        self.assertIn(e_mess_2, response2.content)
        self.assertEqual(response2.status_code, 200)

    def test_image_size_check(self):
        '''
        Test that an image of width pixel lower than 1280 and height pixel
        lower than 700 cannot be added.
        '''
        mock_image = image('test_image_4.jpeg')
        form = {"photo": mock_image, "carousel_color": "red",
                "phone_name": "test_phone_4", "phone_tag": "test_phone_tag4",
                "text_color": "white"}
        response = self.elena.post(self.add_url, form)
        self.assertIn(str.encode(landing_page_error.format(225, 225)),
                      response.content)
        self.assertEqual(response.status_code, 200)


class PhoneCategoryListViewsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneCategoryListViewsTestCase, self).setUp()
        self.add_url = "/admin/front/phonecategorylist/add/"

    def test_uniqueness(self):
        '''
        Test  that it informs the admin user that the entered value should be
        unique hence preventing the presence of two similar names.
        '''
        form = {"phone_category": "Iphone"}
        response = self.elena.post(self.add_url, form)
        e_mess_1 = "The phone category Iphone already exists"
        self.assertContains(response, e_mess_1)

    def test_limitation_on_adding(self):
        '''
        Test that a limitation exists to the number of Phone Categories that
        can be added.
        '''
        form1 = {"phone_category": "Phone1"}
        form2 = {"phone_category": "Phone2"}
        response1 = self.elena.post(self.add_url, form1)
        response2 = self.elena.post(self.add_url, form2)
        self.assertEqual(response1.status_code, 302)
        self.assertContains(response2, phone_category_error)

    def test_display_of_phone_categories(self):
        '''
        Test that Phone categories are being displayed on the front page of
        the application
        '''
        self.elena.post(self.add_url, {'phone_category': "Extra"})
        response = self.client.get('/')
        self.assertContains(response, "Iphone")
        self.assertContains(response, "Android")
        self.assertContains(response, "Tablet")
        self.assertContains(response, "Extra")

    def test_admin_view(self):
        response = self.elena.get('/admin', follow=True)
        self.assertContains(response, "Phone Categories")
        self.assertContains(response, "Phones")
        self.assertContains(response, "Currencies")


class PhoneListViewsTestCase(BaseTestCase):

    def setUp(self):
        super(PhoneListViewsTestCase, self).setUp()

    def test_shillings_value_is_returned(self):
        Currency.objects.create(currency_abbreviation="£$Shs",
                                currency_long_form="Pound")
        currency = Currency.objects.get(currency_long_form="Pound")
        PhoneList.objects.create(category=self.iphone, currency=currency,
                                 price=30, phone_name="Iphone 6")
        response = self.client.get("/phone_category/{}/"
                                   .format(self.iphone.pk))
        self.assertContains(response, "£$Shs")

    def test_limit_on_image_size(self):
        '''
        Test that an image of dimensions 225 by 225 cannot be added and that it
        gives the correct error message.
        '''
        mock_image = image('test_image_4.jpeg')
        form = {"phone_image": mock_image, "phone_name": "PhoneTest1"}
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertIn(str.encode(phone_list_error.format(225, 225)),
                      response.content)

    def test_creation_of_entry(self):
        '''
        Test that an image can be created successfully for a phone list.
        '''
        mock_image = image('test_image_5.png')
        form = {"phone_image": mock_image, "phone_name": "Phone_ImageV",
                "price": 250, "category": self.android.pk,
                "currency": self.currency_v.pk,
                "size_sku":  self.size_android.pk}
        response = self.elena.post('/admin/front/phonelist/add/', form,
                                   follow=True)
        phone_object = PhoneList.objects.get(phone_name="Phone_ImageV")
        self.assertContains(response, "The phone list ")
        self.assertContains(response, str(phone_object))
        self.assertContains(response, "was added successfully.")
        self.assertRedirects(response, "/admin/front/phonelist/")


class PhoneMemorySizeViewsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneMemorySizeViewsTestCase, self).setUp()

    def test_views_according_to_phone_category(self):
        data = {self.iphone.pk: ["8 GB", "24 GB"],
                self.android.pk: ["16 GB", "8 GB"],
                self.tablet.pk: ["24 GB", "16 GB"]}
        for key in data:
            response = self.client.get('/phone_category/{}/'.format(key))
            self.assertContains(response, data[key][0])
            self.assertNotContains(response, data[key][1])


class ClientViewsTestCase(BaseTestCase):
    def setUp(self):
        super(ClientViewsTestCase, self).setUp()

    def create_phone(self, image_name, category, size, name, currency):
        mock_image = image(image_name)
        PhoneList.objects.create(category=category, phone_image=mock_image,
                                 phone_name=name, currency=currency, price=25,
                                 size_sku=size)

    def test_rendering_on_page_view(self):
        mock_image = image("test_image_1.jpeg")
        LandingPageImage.objects.create(phone_name="ViewPhone",
                                        phone_tag="ViewPhone1_Tag",
                                        photo=mock_image, pk=4)
        response = self.client.get('/')
        self.assertContains(response, "Iphone")
        self.assertContains(response, "Android")
        self.assertContains(response, "/media/test_image_1")

    def test_phone_category_view(self):
        self.create_phone("test_image_5.png", self.iphone, self.size_iphone,
                          "LaIphone", self.currency_v)
        response = self.client.get('/phone_category/{}/'
                                   .format(self.iphone.pk))
        self.assertContains(response, "V$")
        self.assertContains(response, 25)
        self.assertContains(response, "LaIphone")
        self.assertContains(response, "/media/test_image_5")

    def test_phone_category_size_view(self):
        test_variables = {"a": [self.iphone.pk, "8 GB", "16 GB"],
                          "b": [self.android.pk, "16 GB", "24 GB"],
                          "c": [self.tablet.pk, "24 GB", "8 GB"]}
        for key in test_variables:
            response = self.client.get('/phone_category/{}/'
                                       .format(test_variables[key][0]))
            self.assertContains(response, test_variables[key][1])
            self.assertNotContains(response, test_variables[key][2])

    def test_size_search(self):
        data_1 = {"a": [self.iphone, self.size_iphone, "Iphone1"],
                  "b": [self.android, self.size_android, "Android1"],
                  "c": [self.tablet, self.size_tablet, "Tablet1"]}
        for key in data_1:
            self.create_phone("test_image_5.png", data_1[key][0],
                              data_1[key][1], data_1[key][2], self.currency_v)
        data_2 = {"a": [self.iphone.pk, self.size_iphone.pk, "Iphone1",
                        "Android1", "with a size of".format(self.size_iphone)],
                  "b": [self.android.pk, self.size_android.pk, "Android1",
                        "Tablet1", "with a size of".format(self.size_iphone)],
                  "c": [self.tablet.pk, self.size_tablet.pk, "Tablet1",
                        "Iphone1", "with a size of".format(self.size_iphone)],
                  }
        for key in data_2:
            response = self.client.get('/phone_category/{}/{}/'
                                       .format(data_2[key][0], data_2[key][1]))
            self.assertContains(response, data_2[key][2])
            self.assertNotContains(response, data_2[key][3])
            self.assertContains(response, data_2[key][4])

    def test_size_filter(self):
        response = self.client.get('/sizes', {"id": self.android.pk})
        self.assertContains(response, self.size_android.pk)
        self.assertContains(response, self.size_android)


def image(name):
    image_path = BASE_DIR + '/media/' + name
    mock_image = SimpleUploadedFile(name=name,
                                    content=open(image_path, 'rb').read(),
                                    content_type='image/jpeg')
    return mock_image
