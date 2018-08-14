from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from front.base_test import *
from hirola.settings.base import BASE_DIR


class LandingPageCacheTest(BaseTestCase):

    def setUp(self):
        super(LandingPageCacheTest, self).setUp()

    def tearDown(self):
        cache.delete_many(['landing_page_images', 'phone_categories'])

    def landing_pg_image_cache_exists(self):
        '''
        Access the landing page and determine that a cache for landing page
        images is created after accessing the page.
        '''
        self.client.get('/')
        cache_after_access = cache.get('landing_page_images')
        self.assertNotEqual(cache_after_access, None)

    def phone_category_cache_exists(self):
        '''
        Access the landing page and determine that a cache for phone categories
        is created after accessing the page.
        '''
        self.client.get('/')
        cache_after_access = cache.get('phone_categories')
        self.assertNotEqual(cache_after_access, None)

    def test_cache_set_on_client_access(self):
        '''
        Test that the cache is set after a client accesses the page_view url.
        '''
        lp_cache_before_access = cache.get('landing_page_images')
        self.assertEqual(lp_cache_before_access, None)
        pc_cache_before_access = cache.get('phone_categories')
        self.assertEqual(pc_cache_before_access, None)
        self.landing_pg_image_cache_exists()
        self.phone_category_cache_exists()

    def test_cache_cleared_on_add(self):
        '''
        Test that the cache for landing page images is deleted when a landing
        page image is added. Ideally the test should operate in a scenario
        where the cache already exists.
        '''
        self.landing_pg_image_cache_exists()
        mock_image = image('test_image_1.jpeg')
        form = landing_page_form(mock_image, 5, ["amber", "black"])
        add_url = "/admin/front/landingpageimage/add/"
        response = self.elena.post(add_url, form)
        get_image = LandingPageImage.objects.get(phone_name="test_phone_name5")
        self.assertEqual(get_image.phone_tag, "test_phone_tag5")
        cache_after_add = cache.get('landing_page_images')
        self.assertEqual(cache_after_add, None)
        self.phone_category_cache_exists()
        category_add_url = "/admin/front/phonecategorylist/add/"
        category_form = {"phone_category": "Phone1"}
        response = self.elena.post(category_add_url, category_form)
        self.assertEqual(response.status_code, 302)
        category_cache_after_add = cache.get('phone_categories')
        self.assertEqual(category_cache_after_add, None)

    def test_cache_cleared_on_edit(self):
        '''
        Test that the cache for landing page images is deleted when a landing
        page image is edited. Ideally the test should operate in a scenario
        where the cache already exists.
        '''
        self.landing_pg_image_cache_exists()
        get_image = LandingPageImage.objects.get(phone_name='test_phone_name2')
        self.assertEqual(get_image.phone_tag, 'test_phone_tag2')
        edit_url = "/admin/front/landingpageimage/{}/change/"
        mock_image = image('test_image_3.jpeg')
        form = landing_page_form(mock_image, 3, ["green", "black"])
        response = self.elena.post(edit_url.format(get_image.pk), form)
        cache_after_add = cache.get('landing_page_images')
        self.assertEqual(cache_after_add, None)
        self.phone_category_cache_exists()
        category_edit_url = "/admin/front/phonecategorylist/{}/change/"
        category_form = {"phone_category": "Phone1"}
        response = self.elena.post(category_edit_url.format(self.iphone.pk),
                                   category_form)
        self.assertEqual(response.status_code, 302)
        category_cache_after_edit = cache.get('phone_categories')
        self.assertEqual(category_cache_after_edit, None)

    def test_cache_cleared_on_delete(self):
        '''
        Test that the cache for landing page images is deleted when a landing
        page image is deleted. Ideally the test should operate in a scenario
        where the cache already exists.
        '''
        self.landing_pg_image_cache_exists()
        get_image = LandingPageImage.objects.get(phone_name='test_phone_name2')
        get_image.delete()
        cache_after_delete = cache.get('landing_page_images')
        self.assertEqual(cache_after_delete, None)
        self.phone_category_cache_exists()
        self.iphone.delete()
        category_cache_after_delete = cache.get('phone_categories')
        self.assertEqual(category_cache_after_delete, None)


class PhoneCategoryViewCacheTest(BaseTestCase):

    def setUp(self):
        self.phone_edit_url = "/admin/front/phonelist/{}/change/"
        super(PhoneCategoryViewCacheTest, self).setUp()

    def tearDown(self):
        cache.clear()

    def phone_cache_exists(self):
        '''
        Access the phone category page for Iphone and determine that the cache
        for phone category is set.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('phones_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)

    def test_cache_set_on_view_access(self):
        '''
        Test that on access of a phone category page the cache for a phone
        category is set.
        '''
        self.phone_cache_exists()

    def test_cache_cleared_on_add(self):
        '''
        Test that when a phone is added that has a category, the cache for
        phone filters with the category being added is deleted.
        '''
        self.phone_cache_exists()
        form = phone_form(self.iphone.pk, self.currency_v.pk,
                          self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        cache_after_add = cache.get('phones_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_add, None)

    def test_edition_category_change(self):
        '''
        Test that if an admin changes the category of a phone from one category
        to another, that the cache of both categories are deleted.
        '''
        # Add a phone with the category Iphone
        form = phone_form(self.iphone.pk, self.currency_v.pk,
                          self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        # Visit the URL for Iphone and ensure a cache is added.
        self.phone_cache_exists()
        # Visit the URL for Android and ensure that a cache exists for Android.
        self.client.get('/phone_category/{}/'.format(self.android.pk))
        cache_after_access = cache.get('phones_{}'.format(self.android.pk))
        self.assertNotEqual(cache_after_access, None)
        # Create input for an edit
        form_2 = phone_form(self.android.pk, self.currency_v.pk,
                            self.size_iphone.pk)
        phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        response = self.elena.post(self.phone_edit_url.format(phone.pk),
                                   form_2)
        cache_after_edit_i = cache.get('phones_{}'.format(self.iphone.pk))
        cache_after_edit_a = cache.get('phones_{}'.format(self.android.pk))
        self.assertEqual(cache_after_edit_i, None)
        self.assertEqual(cache_after_edit_a, None)

    def test_edition_to_none_category(self):
        '''
        Test that if an admin edits a phone and changes its category to None
        that the cache for the previous category it was on will be deleted.
        '''
        form = phone_form(self.iphone.pk, self.currency_v.pk,
                          self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        self.phone_cache_exists()
        phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        form_2 = phone_form("", self.currency_v.pk, self.size_iphone.pk)
        response = self.elena.post(self.phone_edit_url.format(phone.pk),
                                   form_2)
        cache_after_edit = cache.get('phones_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_edit, None)

    def test_edition_to_category(self):
        '''
        Test that if an admin edits a phone that had a None category to an
        existent category that the cache for the existent or newly created
        category will be deleted.
        '''
        form = phone_form("", self.currency_v.pk, self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        self.phone_cache_exists()
        phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        form_2 = phone_form(self.iphone.pk, self.currency_v.pk,
                            self.size_iphone.pk)
        response = self.elena.post(self.phone_edit_url.format(phone.pk),
                                   form_2)
        cache_after_edit = cache.get('phones_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_edit, None)

    def test_phone_deletion(self):
        '''
        Test that when a phone is deleted that belonged to a category, the
        cache with that category id is deleted.
        '''
        form = phone_form(self.iphone.pk, self.currency_v.pk,
                          self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        self.phone_cache_exists()
        get_phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        get_phone.delete()
        cache_after_delete = cache.get("phones_{}".format(self.iphone.pk))
        self.assertEqual(cache_after_delete, None)

    def test_non_categorized_phone_deletion(self):
        '''
        Test that the deletion of a non-categorized phone will be error free.
        '''
        # Create a non-categorized phone
        form = phone_form("", self.currency_v.pk, self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        get_phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        self.assertEqual(get_phone.category, None)
        # Delete the phone
        get_phone.delete()

    def test_edit_non_to_non_categorized_phone(self):
        '''
        Test that editing a non-categorized phone still maintaining its non-cat
        egorized state will bring no errors
        '''
        # Create a non-categorized phone
        form = phone_form("", self.currency_v.pk, self.size_iphone.pk)
        response = self.elena.post('/admin/front/phonelist/add/', form)
        self.assertEqual(response.status_code, 302)
        phone = PhoneList.objects.get(phone_name="Phone_ImageV")
        self.assertEqual(phone.category, None)
        # Edit non-categorized phone
        form_2 = phone_form("", self.currency_v.pk, self.size_android.pk)
        response = self.elena.post(self.phone_edit_url.format(phone.pk),
                                   form_2)
        self.assertEqual(response.status_code, 302)

    def test_category_deletion(self):
        '''
        Test that when a category is deleted the cache for getting the name of
        the category is deleted.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access_c = cache.get('category_{}'.format(self.iphone.pk))
        cache_after_access_p = cache.get('phones_{}'.format(self.iphone.pk))
        cache_after_access_s = cache.get('sizes_{}'.format(self.iphone.pk))
        cache_after_access_pc = cache.get('phone_categories')
        self.assertNotEqual(cache_after_access_c, None)
        self.assertNotEqual(cache_after_access_p, None)
        self.assertNotEqual(cache_after_access_s, None)
        self.assertNotEqual(cache_after_access_pc, None)
        iphone_id = self.iphone.pk
        self.iphone.delete()
        cache_after_delete_c = cache.get('category_{}'.format(iphone_id))
        cache_after_delete_p = cache.get('phones_{}'.format(iphone_id))
        cache_after_delete_s = cache.get('sizes_{}'.format(iphone_id))
        cache_after_delete_pc = cache.get('phone_categories')
        self.assertEqual(cache_after_delete_c, None)
        self.assertEqual(cache_after_delete_p, None)
        self.assertEqual(cache_after_delete_s, None)
        self.assertEqual(cache_after_delete_pc, None)

    def test_category_edition(self):
        '''
        Test that when a category is edited the cache for the category is
        deleted.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('category_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        iphone_id = self.iphone.pk
        form = {"phone_category": "New Category"}
        category_edit_url = "/admin/front/phonecategorylist/{}/change/"
        response = self.elena.post(category_edit_url.format(iphone_id), form)
        self.assertEqual(response.status_code, 302)
        edited_category = PhoneCategoryList.objects.get(pk=self.iphone.pk)
        self.assertEqual(str(edited_category), "New Category")
        cache_after_delete = cache.get('category_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_delete, None)

    def test_cache_size_created(self):
        '''
        Test that the cache for sizes in a particular category is created by
        visiting a view.
        '''
        cache_before_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_before_access, None)
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)

    def test_deletion_of_category_size(self):
        '''
        Test that when a size is deleted with a particular Category that the
        cache for size with the category id is deleted.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        self.size_iphone.delete()
        cache_after_delete = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_delete, None)

    def test_deletion_of_non_category_size(self):
        '''
        Test that this process does not affect the application deletion in any
        negative manner.
        '''
        empty_size = PhoneMemorySize.objects.create(abbreviation="GB",
                                                    size_number=8)
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        empty_size.delete()
        cache_after_delete = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_delete, None)

    def test_addition_of_size_with_category(self):
        '''
        Test that when a size category is being added, the cache of sizes with
        the respective category id needs to be deleted.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        form = {"abbreviation": "AB", "size_number": 22,
                "category": self.iphone.pk}
        response = self.elena.post("/admin/front/phonememorysize/add/", form)
        size = PhoneMemorySize.objects.get(size_number=22)
        self.assertEqual(size.abbreviation, "AB")
        cache_after_delete = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_delete, None)

    def test_addition_of_size_with_non_category(self):
        '''
        Test that when a size without a category is being added, no error
        is raised based on the changes made to the application. Test that
        no cache that existed before is deleted inadvertently.
        '''
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        form = {"abbreviation": "CD", "size_number": 28,
                "category": ""}
        response = self.elena.post("/admin/front/phonememorysize/add/", form)
        self.assertEqual(response.status_code, 302)
        size = PhoneMemorySize.objects.get(size_number=28)
        self.assertEqual(size.abbreviation, "CD")
        cache_after_add = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_add, None)

    def test_edit_size_non_category_to_category(self):
        '''
        Test that when editing a size object that does not contain a category
        to contain an attribute of a category the cache for the size object
        with the category id being added should be deleted.
        '''
        # Add a non-categorized object to be edited.
        form = {"abbreviation": "EF", "size_number": 32,
                "category": ""}
        response = self.elena.post("/admin/front/phonememorysize/add/", form)
        size = PhoneMemorySize.objects.get(size_number=32)
        # Ensure that the cache for iphone category exists () before editing
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        # Edit the non-categorized object.
        size_edit_url = "/admin/front/phonememorysize/{}/change/"
        form = {"abbreviation": "CD", "size_number": 28,
                "category": self.iphone.pk}
        response = self.elena.post(size_edit_url.format(size.pk), form)
        self.assertEqual(response.status_code, 302)
        # Test that the respective cache is deleted
        cache_after_edit = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_edit, None)

    def test_edit_category_to_non_category(self):
        '''
        Test taht when editing a size object that contains a category to not
        contain a category attribute that the cache of the category where it
        existed in is deleted.
        '''
        # Ensure that the cache for iphone category exists () before editing
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access, None)
        # Edit the categorized object.
        size_edit_url = "/admin/front/phonememorysize/{}/change/"
        form = {"abbreviation": "GB", "size_number": 12,
                "category": ""}
        response = self.elena.post(size_edit_url.format(self.size_iphone.pk),
                                   form)
        self.assertEqual(response.status_code, 302)
        size = PhoneMemorySize.objects.get(pk=self.size_iphone.pk)
        self.assertEqual(size.category, None)
        cache_after_edit = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_edit, None)

    def test_edit_category_to_another_category(self):
        '''
        Test that when editing a size object with a category to another
        category that the cache of both sizes are deleted.
        '''
        # Ensure the existence of an iphone cache
        self.client.get('/phone_category/{}/'.format(self.iphone.pk))
        cache_after_access_i = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertNotEqual(cache_after_access_i, None)
        # Ensure the existence of an android cache
        self.client.get('/phone_category/{}/'.format(self.android.pk))
        cache_after_access_a = cache.get('sizes_{}'.format(self.android.pk))
        self.assertNotEqual(cache_after_access_a, None)
        # Edit Android Categorized size to Iphone Categorized
        size_edit_url = "/admin/front/phonememorysize/{}/change/"
        form = {"abbreviation": "GB", "size_number": 21,
                "category": self.iphone.pk}
        response = self.elena.post(size_edit_url.format(self.size_android.pk),
                                   form)
        self.assertEqual(response.status_code, 302)
        size = PhoneMemorySize.objects.get(pk=self.size_android.pk)
        self.assertEqual(size.category, self.iphone)
        # Confirm iphone cache deleted
        cache_after_edit_i = cache.get('sizes_{}'.format(self.iphone.pk))
        self.assertEqual(cache_after_edit_i, None)
        # Confirm android cache deleted
        cache_after_edit_a = cache.get('sizes_{}'.format(self.android.pk))
        self.assertEqual(cache_after_edit_a, None)

    def test_edit_size_non_to_non_category(self):
        '''
        Test that the edition of a non-categorizes size to a non-categorized
        cache will run with error free.
        '''
        # Create a non-categorized object
        form = {"abbreviation": "FG", "size_number": 23,
                "category": ""}
        response = self.elena.post("/admin/front/phonememorysize/add/", form)
        self.assertEqual(response.status_code, 302)
        size = PhoneMemorySize.objects.get(abbreviation="FG")
        self.assertEqual(size.size_number, 23)
        self.assertEqual(size.category, None)
        # Edit the non-categorized object
        size_edit_url = "/admin/front/phonememorysize/{}/change/"
        form = {"abbreviation": "HI", "size_number": 25,
                "category": ""}
        response = self.elena.post(size_edit_url.format(size.pk), form)
        self.assertEqual(response.status_code, 302)
        edited_size = PhoneMemorySize.objects.get(pk=size.pk)
        self.assertEqual(edited_size.size_number, 25)
        self.assertEqual(edited_size.category, None)
        self.assertEqual(edited_size.abbreviation, "HI")


class FooterViewCacheTest(BaseTestCase):

    def setUp(self):
        super(FooterViewCacheTest, self).setUp()

    def tearDown(self):
        cache.clear()

    def get_page_and_set_cache(self):
        '''
        Get to a page and set the cache for the footer. Test that it exists.
        '''
        self.client.get("/about")
        media_cache = cache.get('social_media')
        self.assertNotEqual(media_cache, None)

    def get_none_on_cache(self):
        '''
        When a cache for social media is queried it returns None
        '''
        media_cache = cache.get('social_media')
        self.assertEqual(media_cache, None)

    def create_social_media_object(self):
        '''
        Create an object for social media
        '''
        data = {"url_link": "http://example.com", "name": "example",
                "icon": "fa fa icon"}
        self.elena.post("/admin/front/socialmedia/add/", data)

    def test_setting_of_cache_social_media(self):
        '''
        Test that the 'social_media' cache does not exist and that it is
        created after visting a page.
        '''
        self.get_none_on_cache()
        self.get_page_and_set_cache()

    def test_addition_of_social_media(self):
        '''
        Test that the addition of social media will delete the cache
        '''
        self.get_page_and_set_cache()
        self.create_social_media_object()
        self.get_none_on_cache()

    def test_edition_of_social_media(self):
        '''
        Test that the edition of social media will delete the cache
        '''
        self.create_social_media_object()
        self.get_page_and_set_cache()
        media_object = SocialMedia.objects.get(name="example")
        url = "/admin/front/socialmedia/{}/change/".format(media_object.pk)
        data_2 = {"url_link": "http://example.com", "name": "another_name",
                  "icon": "fa fa icon"}
        self.elena.post(url, data_2)
        self.assertEqual(SocialMedia.objects.get(pk=media_object.pk).name,
                         "another_name")
        self.get_none_on_cache()

    def test_deletion_of_social_media(self):
        '''
        Test that the deletion of social media will delete the cache
        '''
        self.create_social_media_object()
        self.get_page_and_set_cache()
        media_object = SocialMedia.objects.get(name="example")
        media_object.delete()
        self.get_none_on_cache()


def phone_form(category, currency, size):
    mock_image = image('test_image_5.png')
    form = {"phone_image": mock_image, "phone_name": "Phone_ImageV",
            "price": 250, "category": category,
            "currency": currency,
            "size_sku": size}
    return form
