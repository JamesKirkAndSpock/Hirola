from front.base_test import *
from front.admin import ShippingAddressInline


class Orders(BaseTestCase):

    def setUp(self):
        super(Orders, self).setUp()

    def test_shipping_address(self):
        '''
        Test that when you visit an add page for an order:
            - That the shipping address row does not have an add another button.
        '''
        self.assertEqual(ShippingAddressInline.max_num, 1)
        get_response = self.elena.get("/admin/front/order/add/")
        self.assertContains(get_response, "Shipping address")
