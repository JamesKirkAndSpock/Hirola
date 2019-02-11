from front.base_test import (BaseTestCase, PhoneList, PhonesColor, image,
                             Currency, cache)
from front.errors import (category_image_error, phone_category_error)
from .test_users import UserSignupTestCase
from .test_cache import phone_form


class LandingPageViewsTestCase(BaseTestCase):
    def setUp(self):
        super(LandingPageViewsTestCase, self).setUp()

    def test_hot_deals_rendering(self):
        '''
        Test that Hot Deals are rendered on the landing page.
        '''
        before_response = self.client.get("/")
        self.assertNotContains(before_response, "Hot deals!")
        self.elena.post('/admin/front/hotdeal/add/', {"item": self.iphone_6.pk})
        response = self.client.get("/")
        self.assertContains(response, "Hot deals!")
        self.assertContains(response, "Iphone 6")
        self.assertContains(response, 30)
        self.assertContains(response, "fab fa-apple")
        self.assertContains(response, "/media/phones/test_image_5_")
        self.assertContains(response, "/profile/{}/".format(self.iphone_6.pk))

    def test_non_hot_deals_rendering(self):
        '''
        Test that if a Hot Deal is not in stock or its quantity is zero:
            - That it is  not rendered on the landing page
            - That any hot deal with the opposite is rendered on the landing page
        '''
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="LG Razor J7",
                                 size_sku=self.size_android)
        self.lg_razor = PhoneList.objects.get(phone_name="LG Razor J7")
        PhonesColor.objects.create(phone=self.lg_razor,
                                   size=self.any_phone_size, price=10000,
                                   quantity=1, is_in_stock=True,
                                   color=self.color_one)
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="Samsung S8",
                                 size_sku=self.size_android)
        self.samsung_s8 = PhoneList.objects.get(phone_name="Samsung S8")
        PhonesColor.objects.create(phone=self.samsung_s8,
                                   size=self.size_android, price=10000,
                                   quantity=0, is_in_stock=True,
                                   color=self.color_one)
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="Samsung Note 5",
                                 size_sku=self.size_android)
        self.samsung_n5 = PhoneList.objects.get(phone_name="Samsung Note 5")
        PhonesColor.objects.create(phone=self.samsung_n5,
                                   size=self.any_phone_size, price=10000,
                                   quantity=1, is_in_stock=False,
                                   color=self.color_one)
        self.elena.post('/admin/front/hotdeal/add/', {"item": self.lg_razor.pk})
        self.elena.post('/admin/front/hotdeal/add/', {"item": self.samsung_s8.pk})
        self.elena.post('/admin/front/hotdeal/add/', {"item": self.samsung_n5.pk})
        get_response = self.client.get("/")
        self.assertContains(get_response, "LG Razor J7")
        self.assertNotContains(get_response, "Samsung S8")
        self.assertNotContains(get_response, "Samsung Note 5")

    def test_limit_on_image_size(self):
        '''
        Test that when adding a category, with an image of dimensions 225 by 225:
            - The page will not redirect as the image cannot be added
            - An error message is raised
        Test that when adding a category, with an image of dimensions 200 by 200:
            - The page will redirect as the image has been added
        '''
        mock_image = image('test_image_1.jpeg')
        form = {"category_image": mock_image, "phone_category": "CategoryTest1"}
        response = self.elena.post('/admin/front/phonecategory/add/', form)
        self.assertIn(str.encode(category_image_error.format(959, 1280)),
                      response.content)
        self.assertEqual(response.status_code, 200)
        mock_image_2 = image('test_image_6.png')
        form_2 = {"category_image": mock_image_2, "phone_category": "CategoryTest1"}
        response = self.elena.post('/admin/front/phonecategory/add/', form_2)
        self.assertRedirects(response, "/admin/front/phonecategory/", 302)

    def test_category_image_rendering_on_view(self):
        mock_image_2 = image('test_image_6.png')
        form_2 = {"category_image": mock_image_2, "phone_category": "CategoryTest1"}
        self.elena.post('/admin/front/phonecategory/add/', form_2)
        response = self.client.get("/")
        self.assertContains(response, "src=\"/media/phone_categories/test_image_6")


class PhoneCategoryViewsTestCase(BaseTestCase):
    def setUp(self):
        super(PhoneCategoryViewsTestCase, self).setUp()
        self.category_image = image('test_image_6.png')
        self.add_url = "/admin/front/phonecategory/add/"

    def test_uniqueness(self):
        '''
        Test  that it informs the admin user that the entered value should be
        unique hence preventing the presence of two similar names.
        '''
        form = {"phone_category": "Iphone", "category_image": self.category_image}
        response = self.elena.post(self.add_url, form)
        e_mess_1 = "The phone category Iphone already exists"
        self.assertContains(response, e_mess_1)

    def test_limitation_on_adding(self):
        '''
        Test that a limitation exists to the number of Phone Categories that
        can be added.
        '''
        form1 = {"phone_category": "Phone1", "category_image": self.category_image}
        form2 = {"phone_category": "Phone2", "category_image": self.category_image}
        response1 = self.elena.post(self.add_url, form1)
        response2 = self.elena.post(self.add_url, form2)
        self.assertEqual(response1.status_code, 302)
        self.assertContains(response2, phone_category_error)

    def test_display_of_phone_categories(self):
        '''
        Test that Phone categories are being displayed on the front page of
        the application
        '''
        self.elena.post(self.add_url, {'phone_category': "Extra",
                        "category_image": self.category_image})
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

    def test_social_media_on_view(self):
        '''
        Test that Social Media Links can be seen on the Phone categories view.
        '''
        add_url = "/admin/front/socialmedia/add/"
        data = {"url_link": "https://facebook.com", "icon": "fa fa-facebook",
                "name": "Facebook"}
        self.elena.post(add_url, data)
        response = self.client.get('/phone_category/{}/'.format(self.iphone.id))
        facebook_url = "<a href=\"https://facebook.com\" target=\"_blank\">"
        facebook_data_icon_name = "<i class=\"fa fa-facebook\"></i> Facebook</a>"
        self.assertContains(response, facebook_url)
        self.assertContains(response, facebook_data_icon_name)


class PhoneListViewsTestCase(BaseTestCase):

    def setUp(self):
        super(PhoneListViewsTestCase, self).setUp()

    def test_shillings_value_is_returned(self):
        Currency.objects.create(currency_abbreviation="£$Shs",
                                currency_long_form="Pound")
        currency = Currency.objects.get(currency_long_form="Pound")
        PhoneList.objects.create(category=self.iphone, currency=currency,
                                 price=30, phone_name="Iphone 8S")
        phone = PhoneList.objects.get(phone_name="Iphone 8S")
        PhonesColor.objects.create(phone=phone, size=self.any_phone_size,
                                   price=10000, color=self.color_one,
                                   quantity=4, is_in_stock=True)
        response = self.client.get("/phone_category/{}/".
                                   format(self.iphone.pk))
        self.assertContains(response, "£$Shs")

    def test_creation_of_entry(self):
        '''
        Test that an image can be created successfully for a phone list.
        '''
        mock_image = image('test_image_5.png')
        form = phone_form(self.iphone.pk, self.currency_v.pk,
                          self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form,
                                   follow=True)
        phone_object = PhoneList.objects.get(phone_name="Phone_ImageV")
        self.assertContains(response, "The phone list ")
        self.assertContains(response, str(phone_object))
        self.assertContains(response, "was added successfully.")
        self.assertRedirects(response, "/admin/front/phonelist/")

    def test_phones_rendering(self):
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="LG Razor J7",
                                 size_sku=self.size_android)
        self.lg_razor = PhoneList.objects.get(phone_name="LG Razor J7")
        PhonesColor.objects.create(phone=self.lg_razor, size=self.size_android,
                                   price=10000, quantity=1, is_in_stock=True,
                                   color=self.color_one)
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="Samsung S8",
                                 size_sku=self.size_android)
        self.samsung_s8 = PhoneList.objects.get(phone_name="Samsung S8")
        PhonesColor.objects.create(phone=self.samsung_s8,
                                   size=self.any_phone_size, price=10000,
                                   quantity=0, is_in_stock=True,
                                   color=self.color_one)
        PhoneList.objects.create(category=self.android,
                                 currency=self.currency_v, price=8000,
                                 phone_name="Samsung Note 5",
                                 size_sku=self.size_android)
        self.samsung_n5 = PhoneList.objects.get(phone_name="Samsung Note 5")
        PhonesColor.objects.create(phone=self.samsung_n5,
                                   size=self.any_phone_size, price=10000,
                                   quantity=1, is_in_stock=False,
                                   color=self.color_one)
        get_response = self.client.get("/phone_category/{}/".
                                       format(self.android.pk))
        self.assertContains(get_response, "LG Razor J7")
        self.assertNotContains(get_response, "Samsung S8")
        self.assertNotContains(get_response, "Samsung Note 5")


# class PhoneMemorySizeViewsTestCase(BaseTestCase):
#     def setUp(self):
#         super(PhoneMemorySizeViewsTestCase, self).setUp()

#     def test_views_according_to_phone_category(self):
#         data = {self.iphone.pk: ["8 GB", "24 GB"],
#                 self.android.pk: ["16 GB", "8 GB"],
#                 self.tablet.pk: ["24 GB", "16 GB"]}
#         for key in data:
#             response = self.client.get('/phone_category/{}/'.format(key))
#             self.assertContains(response, data[key][0])
#             self.assertNotContains(response, data[key][1])


class ClientViewsTestCase(BaseTestCase):
    def setUp(self):
        super(ClientViewsTestCase, self).setUp()

    def create_phone(self, image_name, category, size, name, currency):
        mock_image = image(image_name)
        PhoneList.objects.create(category=category, main_image=mock_image,
                                 phone_name=name, currency=currency, price=25,
                                 size_sku=size)
        phone = PhoneList.objects.get(phone_name=name)
        PhonesColor.objects.create(phone=phone, size=self.size_android,
                                   price=10000, color=self.color_one,
                                   quantity=5, is_in_stock=True)

    # def test_rendering_on_page_view(self):
    #     mock_image = image("test_image_1.jpeg")
    #     LandingPageImage.objects.create(phone_name="ViewPhone",
    #                                     phone_tag="ViewPhone1_Tag",
    #                                     photo=mock_image, pk=4)
    #     response = self.client.get('/')
    #     self.assertContains(response, "Iphone")
    #     self.assertContains(response, "Android")
    #     self.assertContains(response, "/media/test_image_1")

    def test_phone_category_view(self):
        self.create_phone("test_image_5.png", self.iphone, self.size_iphone,
                          "LaIphone", self.currency_v)
        response = self.client.get('/phone_category/{}/'
                                   .format(self.iphone.pk))
        self.assertContains(response, "V$")
        self.assertContains(response, 25)
        self.assertContains(response, "LaIphone")
        self.assertContains(response, "/media/phones/test_image_5")

    # def test_phone_category_size_view(self):
    #     test_variables = {"a": [self.iphone.pk, "8 GB", "16 GB"],
    #                       "b": [self.android.pk, "16 GB", "24 GB"],
    #                       "c": [self.tablet.pk, "24 GB", "8 GB"]}
    #     for key in test_variables:
    #         response = self.client.get('/phone_category/{}/'
    #                                    .format(test_variables[key][0]))
    #         self.assertContains(response, test_variables[key][1])
    #         self.assertNotContains(response, test_variables[key][2])

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


class AboutPageViewsTestCase(BaseTestCase):
    def setUp(self):
        super(AboutPageViewsTestCase, self).setUp()

    def test_phone_categories_rendered(self):
        '''
        Test that phone categories from the cache or from the database are
        rendered on the about page.
        '''
        response = self.client.get('/about')
        self.assertContains(response, "Iphone")
        self.assertContains(response, "Android")
        self.assertContains(response, "Tablet")


class FooterViewTestCase(BaseTestCase):
    def setUp(self):
        super(FooterViewTestCase, self).setUp()

    def tearDown(self):
        cache.clear()

    def test_admin_view(self):
        '''
        Test that when visiting the admin view the Meta name for the Social
        Media Model is as indicated on the models class
        '''
        response = self.elena.get('/admin', follow=True)
        self.assertContains(response, "Social Media")

    def test_category_data(self):
        '''
        Test that category links and views are available on the footer
        '''
        response = self.client.get('/about')
        iphone_data = "<a href=\"/phone_category/{}\">Buy Iphone</a>".format(
            self.iphone.id)
        android_data = "<a href=\"/phone_category/{}\">Buy Android</a>".format(
            self.android.id)
        tablet_data = "<a href=\"/phone_category/{}\">Buy Tablet</a>".format(
            self.tablet.id)
        self.assertContains(response, iphone_data)
        self.assertContains(response, android_data)
        self.assertContains(response, tablet_data)

    def test_social_media_data(self):
        '''
        Test that the social media data is rendered properly
        '''
        data = {"url_link": "http://example.com", "name": "example",
                "icon": "fa fa icon"}
        self.elena.post("/admin/front/socialmedia/add/", data)
        response = self.client.get('/about')
        example_data_url = "<a href=\"http://example.com\" target=\"_blank\">"
        example_data_icon_name = "<i class=\"fa fa icon\"></i> example</a>"
        self.assertContains(response, example_data_icon_name)
        self.assertContains(response, example_data_url)

    def test_social_media_object_view(self):
        '''
        Test that the social media objects on the admin view are human readable
        '''
        data = {"url_link": "http://example.com", "name": "Example",
                "icon": "fa fa icon"}
        self.elena.post("/admin/front/socialmedia/add/", data)
        response = self.elena.get("/admin/front/socialmedia/")
        self.assertContains(response, "Example")


class NewsItemTestCase(BaseTestCase):

    def setUp(self):
        super(NewsItemTestCase, self).setUp()

    def test_news_items_rendered(self):
        """
        Test that news item from db has been rendered on the news page.
        """
        response = self.client.get('/news')
        self.assertContains(response, 'Teke rocks')
        self.assertContains(response, 'The standard online')
        self.assertContains(response, 'https://www.sde.com')
