"""Tests hotdeal backend."""
import json
from front.base_test import BaseTestCase
from front.models import HotDeal


class HotDealTestCase(BaseTestCase):
    """Tests backend logic for hotdeal feature."""

    def setUp(self):
        super(HotDealTestCase, self).setUp()
        self.create_hotdeal()

    def test_all_data_rendered(self):
        """
        Test that on the hotdeal page
            -   all the data about the hotdeal item has been rendered.
        """
        hotdeal = HotDeal.objects.get(item=self.samsung_note_5_rose_gold)
        response = self.client.get("/hot_deal/{}/".format(
            hotdeal.id))
        self.assertContains(response, '25000')
        self.assertContains(response, 'Color: Red')
        self.assertContains(response, 'Size: 16 GB Android')
        img = "<img id=\"main_image_src\" src=\"/media/{}\" />".\
            format(self.samsung_note_5_rose_gold.main_image)
        self.assertContains(response, img)
        img_2 = "<li id=\"main_image_data_thumb\" data-thumb=\"/media/{}\">".\
            format(self.samsung_note_5_rose_gold.main_image)
        self.assertContains(response, img_2)

    def test_get_total_on_quantity_change(self):
        """
        Test that on the hot deals page
            - when the hotdeal item quantity is changed,
              the total price changes too.
        """
        data = {
            'qty': 2,
            'phone_model_item': self.samsung_note_5.id
        }
        response = self.client.get('/hot_deal_quantity_change', data)
        self.assertEqual(json.loads(response.content)['total_cost'], '50000')
        self.assertEqual(json.loads(response.content)['currency'], 'V$')

    def create_hotdeal(self):
        """Create a hot deal."""
        HotDeal.objects.create(item=self.samsung_note_5_rose_gold)
